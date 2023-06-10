import json
import pika
import datetime

from typing import Optional, List

from django.db.models import Q, Min, QuerySet
from django.utils import timezone

from common.rabbitmq.base_sync import BaseSync

from avito_parse.models import AvitoUserOfferWatcher, AvitoCategory
from avito_parse.selenium_parser import AvitoOffersParser
from avito_parse.filter_forms.transport import AvitoParsedOffer


class ParsedOffersBetweenWatchersSync(BaseSync):
    """
    Запускает парсер
    фильтрует объявление для пользователей
    """

    def __init__(self, parser: AvitoOffersParser, exclude_offers_links: list, logger):
        self.parser = parser

        self.exclude_offers_links = exclude_offers_links

        self.parsing_city_slug = parser.city_slug
        self.parsing_search_radius = parser.search_radius
        self.log_prefix = (
            f"CITY_SLUG = {parser.city_slug}, SEARCH_RADIUS = {parser.search_radius}:"
        )
        self.logger = logger

    def check_offers_for_watchers(self) -> Optional[List[str]]:
        offer_watchers_query = Q(
            is_deleted=False,
            city_url_slug=self.parsing_city_slug,
            search_radius=self.parsing_search_radius
        )

        search_before_date = self._get_last_offer_datetime_for_search_by_query(
            offers_watchers_query=offer_watchers_query
        )
        self.logger.info(f"{self.log_prefix} search_before_date = {search_before_date}")

        if not search_before_date:
            return

        parsed_offers = self.parser.get_parsed_offers(
            search_before_date=search_before_date,
            search_before_links=self.exclude_offers_links
        )
        self.logger.info(f"{self.log_prefix} Parsed {len(parsed_offers)} offers: {parsed_offers}")
        if not parsed_offers:
            return

        watchers = (
            AvitoUserOfferWatcher.objects
            .select_related("filter", "category")
            .filter(offer_watchers_query & Q(telegram_user__need_to_notify=True))
        )
        self.logger.info(f"{self.log_prefix} Watchers count: {len(watchers)}")
        if not watchers:
            return

        new_parsed_offers_links = self._sync_watchers_and_parsed_offers(
            parsed_offers=parsed_offers,
            watchers=watchers
        )

        last_date = parsed_offers[0].show_up_date_time
        self.logger.info(f"{self.log_prefix} Update last_checked_offer_datetime: {last_date}")
        watchers.update(last_checked_offer_datetime=last_date)

        return new_parsed_offers_links

    @staticmethod
    def _get_last_offer_datetime_for_search_by_query(
            offers_watchers_query: Q
    ) -> Optional[datetime.datetime]:

        last_checked_offer_datetime_by_slug = (
            AvitoUserOfferWatcher.objects
            .filter(offers_watchers_query)
            .annotate(Min("last_checked_offer_datetime"))
            .values("last_checked_offer_datetime__min")
            .first()
        )
        if last_checked_offer_datetime_by_slug:
            last_checked_offer_datetime = last_checked_offer_datetime_by_slug["last_checked_offer_datetime__min"]
            search_before_date = last_checked_offer_datetime.astimezone(tz=timezone.get_current_timezone())

            # на 5 минут погрешность, чтобы не упустить объявления появившиеся с задержкой
            search_before_date -= datetime.timedelta(minutes=5)

            return search_before_date

    def _sync_watchers_and_parsed_offers(
            self,
            parsed_offers: List[AvitoParsedOffer],
            watchers: QuerySet[AvitoUserOfferWatcher]
    ) -> List[str]:
        new_parsed_offers_links = []
        need_to_send_offers_for_users = []
        for parsed_offer in parsed_offers:
            if parsed_offer.link in self.exclude_offers_links:
                self.logger.info(f"{self.log_prefix} SKIP OFFER: {parsed_offer}")
                continue

            new_parsed_offers_links.append(parsed_offer.link)

            for watcher in watchers:
                filter_form_service = AvitoCategory.FILTER_FORM_CLASS_MAP[watcher.category.filter_form]
                if filter_form_service.parsed_offer_is_match_filter(
                        parsed_offer=parsed_offer,
                        specific_filter=watcher.filter.specific_filter
                ):
                    need_to_send_offers_for_users.append(
                        {
                            "user_id": watcher.telegram_user_id,
                            "parsed_offer": {
                                "title": parsed_offer.title,
                                "car_parameters": parsed_offer.car_parameters,
                                "easy_to_read_price": parsed_offer.easy_to_read_price,
                                "city": parsed_offer.city,
                                "show_up_time_ago": parsed_offer.show_up_time_ago,
                                "link": parsed_offer.link,
                            }
                        }
                    )
        self.logger.info(f"{self.log_prefix} Found match offers by watchers, count: {len(need_to_send_offers_for_users)}")
        if need_to_send_offers_for_users:
            self._publish_users_offers_for_notify(need_to_send_offers_for_users=need_to_send_offers_for_users)

        return new_parsed_offers_links

    def _publish_users_offers_for_notify(self, need_to_send_offers_for_users: List[dict]) -> None:
        self.logger.info(f"{self.log_prefix} Send notifications, count: {len(need_to_send_offers_for_users)}")

        # обработчик отправляющий уведомления
        self.connect_mq(heartbeat=60 * 2)
        self.mq_channel.basic_publish(
            exchange=self.BOT_EXCHANGE,
            routing_key=self.BOT__SEND_OFFERS_QUEUE,
            body=json.dumps(need_to_send_offers_for_users),
            properties=pika.BasicProperties(delivery_mode=2),
        )
