import logging
import asyncio
import time

from django.core.management.base import BaseCommand
from django.db.models import Min
from django.utils.timezone import get_current_timezone, localtime

from avito_parse.selenium_parser import AvitoOffersParser, AvitoParsedOffer
from avito_parse.models import AvitoUserOfferWatcher, AvitoCategory

from bot.bot import bot


async def send_parsed_offer_to_user(tg_user_id: int, parsed_offer: AvitoParsedOffer):
    message = (
        f"{parsed_offer.title}\n"
        f"{parsed_offer.easy_to_read_price.strip()}\n"
        f"{parsed_offer.show_up_time_ago}\n\n"
        f"Ссылка:\n{parsed_offer.link}"
    )
    return await bot.send_message(tg_user_id, message)


async def send_parsed_offers_to_users(list_of_users):
    tasks = []
    for data in list_of_users:
        tasks.append(asyncio.create_task(
            send_parsed_offer_to_user(tg_user_id=data["user_id"], parsed_offer=data["parsed_offer"]))
        )
    logging.info(f"Send parsed to: {list_of_users}")
    results = await asyncio.gather(*tasks)

    for result in results:
        logging.info(f"Message sended: {result}")


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.avito_offers_parser = AvitoOffersParser(
            city_slug="chelyabinsk",
            category_slug="avtomobili",
            search_radius=200
        )

    def handle(self, *args, **options):
        logging.info("Start avito_parse")

        try:
            while True:
                logging.info("Start avito_parse iteration")
                last_checked_offer_datetime = (
                    AvitoUserOfferWatcher.objects
                    .filter(is_deleted=False)
                    .annotate(Min("last_checked_offer_datetime"))
                    .values("last_checked_offer_datetime__min")
                    .first()
                )

                if last_checked_offer_datetime:
                    last_checked_offer_datetime = last_checked_offer_datetime["last_checked_offer_datetime__min"]
                    search_before_date = last_checked_offer_datetime.astimezone(tz=get_current_timezone())
                    logging.info(f"Parse: search_before_date = {search_before_date}")

                    parsed_offers = self.avito_offers_parser.get_parsed_offers(
                        search_before_date=search_before_date
                    )
                    logging.info(f"Parsed {len(parsed_offers)} offers: {parsed_offers}")
                    if parsed_offers:
                        watchers = (
                            AvitoUserOfferWatcher.objects
                            .select_related("filter", "category")
                            .filter(is_deleted=False)
                        )
                        logging.info(f"Watchers count: {len(watchers)}")

                        need_to_send_notification = []
                        for parsed_offer in parsed_offers:
                            for watcher in watchers:
                                filter_form_service = AvitoCategory.FILTER_FORM_CLASS_MAP[watcher.category.filter_form]

                                if filter_form_service.parsed_offer_is_match_filter(
                                        parsed_offer=parsed_offer,
                                        specific_filter=watcher.filter.specific_filter
                                ):
                                    need_to_send_notification.append(
                                        {
                                            "user_id": watcher.telegram_user_id,
                                            "parsed_offer": parsed_offer,
                                        }
                                    )

                        logging.info(f"Send notifications, count: {len(need_to_send_notification)}")
                        if need_to_send_notification:
                            asyncio.run(send_parsed_offers_to_users(list_of_users=need_to_send_notification))

                        last_date = localtime()
                        logging.info(f"Update last_checked_offer_datetime: {last_date}")
                        watchers.update(last_checked_offer_datetime=last_date)

                time.sleep(1)

        except Exception as e:
            logging.warning(f"Expcetion while parse: {e}")
            self.avito_offers_parser.close_driver()
