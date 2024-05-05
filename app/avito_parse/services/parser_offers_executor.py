import json
import pika
import datetime
import logging

from typing import Optional, List

from django.conf import settings
from django.db.models import Q, Min, QuerySet
from django.utils import timezone

from common.rabbitmq.base_sync import BaseSync

from avito_parse.models import AvitoUserOfferWatcher, AvitoCategory
from avito_parse.selenium_parser import AvitoOffersParser
from avito_parse.filter_forms.transport import AvitoParsedOffer

logger = logging.getLogger("avito_parse")


class ParserOffersExecutor(BaseSync):
    """
    Запускает парсер
    фильтрует объявление для пользователей
    """

    def __init__(self, parser: AvitoOffersParser, exclude_offers_links: list):
        self.parser = parser

        self.exclude_offers_links = exclude_offers_links

        self.parsing_city_slug = parser.city_slug
        self.parsing_search_radius = parser.search_radius
        self.log_prefix = (
            f"ParserOffersExecutor: CITY_SLUG = {parser.city_slug}, SEARCH_RADIUS = {parser.search_radius}:"
        )

    def execute_parse(self) -> List[str]:
        offer_watchers_query = Q(
            is_deleted=False,
            city_url_slug=self.parsing_city_slug,
            search_radius=self.parsing_search_radius
        )

        search_before_date = self._get_last_offer_datetime_for_search_by_query(
            offers_watchers_query=offer_watchers_query
        )
        logger.info(f"{self.log_prefix} search_before_date = {search_before_date}")

        if not search_before_date:
            return []

        parsed_offers = self.parser.get_parsed_offers(
            search_before_date=search_before_date,
            search_before_links=self.exclude_offers_links
        )
        logger.info(f"{self.log_prefix} Parsed {len(parsed_offers)} offers: {parsed_offers}")
        if not parsed_offers:
            return []

        # передаём объявления для фильтрации
        publish_data_to_sync = json.dumps(
            {
                "watchers_city_slug": self.parsing_city_slug,
                "watchers_search_radius": self.parsing_search_radius,
                "parsed_offers": list(map(lambda offer: offer._asdict(), parsed_offers))
            },
            default=str
        )
        logger.info(f"publish_data_to_sync: {publish_data_to_sync}")
        self.connect_mq(heartbeat=60 * 2)
        self.mq_channel.basic_publish(
            exchange=self.BOT_EXCHANGE,
            routing_key=self.BOT__SYNC_WATCHERS_WITH_OFFERS_QUEUE,
            body=publish_data_to_sync,
            properties=pika.BasicProperties(delivery_mode=2),
        )

        return list(map(lambda offer: offer.link, parsed_offers))

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
