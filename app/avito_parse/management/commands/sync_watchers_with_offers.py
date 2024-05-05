import asyncio
import json
import pika
import datetime
import logging

from typing import Optional, List

from django.db.models import Q, Min, QuerySet
from django.utils import timezone

from common.rabbitmq.base_sync import BaseSync

from avito_parse.models import AvitoUserOfferWatcher, AvitoCategory
from avito_parse.selenium_parser import AvitoOffersParser
from avito_parse.filter_forms.transport import AvitoParsedOffer

from django.core.management.base import BaseCommand

from avito_parse.selenium_parser import AvitoParsedOffer
from common.rabbitmq.base_sync import BaseSync

from bot.bot import bot


logger = logging.getLogger("sync_watchers_with_offers")


class Command(BaseSync, BaseCommand):

    # todo multiprocessing
    def handle(self, *args, **options):
        logger.info("Start sync_watchers_with_offers")

        while True:
            self.connect_mq()
            self.mq_channel.basic_qos(prefetch_count=1)
            self.mq_channel.basic_consume(
                on_message_callback=self.callback,
                queue=self.BOT__SYNC_WATCHERS_WITH_OFFERS_QUEUE
            )
            self.mq_channel.start_consuming()

    def callback(self, ch, method, properties, body):
        logger.info(f"body: {body}")
        try:
            offers_to_sync_with_watchers = json.loads(body)
        except json.decoder.JSONDecodeError:
            logger.error(f"Empty offers_to_sync_with_watchers")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        logger.info(f"offers_to_sync_with_watchers: {offers_to_sync_with_watchers}")

        watchers_city_slug = offers_to_sync_with_watchers["watchers_city_slug"]
        watchers_search_radius = offers_to_sync_with_watchers["watchers_search_radius"]
        parsed_offers = self._prepare_parsed_offers(offers_to_sync_with_watchers["parsed_offers"])
        logger.info(watchers_search_radius)
        logger.info(watchers_city_slug)
        logger.info(parsed_offers)

        offer_watchers_query = Q(
            is_deleted=False,
            city_url_slug=watchers_city_slug,
            search_radius=watchers_search_radius
        )
        watchers = (
            AvitoUserOfferWatcher.objects
            .select_related("filter", "category")
            .filter(offer_watchers_query & Q(telegram_user__need_to_notify=True))
        )
        logger.info(f"Watchers count: {len(watchers)}")
        if not watchers:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        self._sync_watchers_and_parsed_offers(
            parsed_offers=parsed_offers,
            watchers=watchers
        )

        last_date = parsed_offers[0].show_up_date_time
        logger.info(f"Update last_checked_offer_datetime: {last_date}")
        watchers.update(last_checked_offer_datetime=last_date)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def _prepare_parsed_offers(self, parsed_offers: list) -> List[AvitoParsedOffer]:
        prepared_parsed_offers = []
        for parsed_offer in parsed_offers:
            parsed_offer["show_up_date_time"] = datetime.datetime.fromisoformat(
                parsed_offer["show_up_date_time"]
            )
            prepared_parsed_offers.append(AvitoParsedOffer(**parsed_offer))
        return prepared_parsed_offers

    def _sync_watchers_and_parsed_offers(
            self,
            parsed_offers: List[AvitoParsedOffer],
            watchers: QuerySet[AvitoUserOfferWatcher]
    ) -> None:

        need_to_send_offers_for_users = []

        for parsed_offer in parsed_offers:
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
                                "price": parsed_offer.price,
                                "city": parsed_offer.city,
                                "show_up_time_ago": parsed_offer.show_up_time_ago,
                                "link": parsed_offer.link,
                            }
                        }
                    )
        logger.info(f"Found match offers by watchers, count: {len(need_to_send_offers_for_users)}")
        if need_to_send_offers_for_users:
            self._publish_users_offers_for_notify(need_to_send_offers_for_users=need_to_send_offers_for_users)

    def _publish_users_offers_for_notify(self, need_to_send_offers_for_users: List[dict]) -> None:
        logger.info(f"publish to send: {need_to_send_offers_for_users}")
        # обработчик отправляющий уведомления
        self.connect_mq(heartbeat=60 * 2)
        self.mq_channel.basic_publish(
            exchange=self.BOT_EXCHANGE,
            routing_key=self.BOT__SEND_OFFERS_QUEUE,
            body=json.dumps(need_to_send_offers_for_users),
            properties=pika.BasicProperties(delivery_mode=2),
        )
