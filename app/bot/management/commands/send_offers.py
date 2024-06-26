import json
import logging
import asyncio

from django.core.management.base import BaseCommand

from bot.bot import bot
from common.rabbitmq.base_sync import BaseSync
from parse_offers.offer_structure import ParsedOffer

logger = logging.getLogger("send_offers")


class Command(BaseSync, BaseCommand):
    def handle(self, *args, **options):
        logger.debug("Start send offers")

        while True:
            self.connect_mq()
            self.mq_channel.basic_qos(prefetch_count=200)
            self.mq_channel.basic_consume(
                on_message_callback=self.callback,
                queue=self.BOT__SEND_OFFERS_QUEUE
            )
            self.mq_channel.start_consuming()

    def callback(self, ch, method, properties, body):
        try:
            users_to_notify_offers = json.loads(body)
        except json.decoder.JSONDecodeError:
            logger.exception(f"Empty users_to_notify_offers", exc_info=True)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        logger.debug(f"GET JSON DATA: {users_to_notify_offers=}")

        loop = asyncio.get_event_loop()

        loop.run_until_complete(
            self.send_parsed_offers_to_users(list_of_users=users_to_notify_offers)
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    async def send_parsed_offers_to_users(self, list_of_users: list):
        tasks = []
        for user_notify_data in list_of_users:
            tasks.append(asyncio.create_task(
                self.send_parsed_offer_to_user(
                    tg_user_id=user_notify_data["user_id"],
                    parsed_offer=ParsedOffer(**user_notify_data["parsed_offer"]))
                )
            )

        await asyncio.gather(*tasks)

    async def send_parsed_offer_to_user(self, tg_user_id: int, parsed_offer: ParsedOffer):
        message = (
            f"{parsed_offer.model_brand}, {parsed_offer.year}\n"
            f"{parsed_offer.car_parameters}\n\n"
            f"<b>{parsed_offer.easy_to_read_price}</b>\n"
            f"<b>{parsed_offer.city}</b>\n"
            f"{parsed_offer.show_up_time_ago}\n\n"
            f"Ссылка:\n{parsed_offer.link}"
        )
        logger.debug(f"Send: {message=}")
        await bot.send_message(tg_user_id, message, parse_mode="HTML")
