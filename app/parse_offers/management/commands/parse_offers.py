import logging
import datetime
import time
import random

from time import sleep

from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Dict, List, Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import localtime

from parse_offers.selenium_parsers.avito_parser import AvitoOffersParser
from parse_offers.models import AvitoUserOfferWatcher
from parse_offers.services.parser_offers_executor import ParserOffersExecutor

logger = logging.getLogger("parse_offers")


@dataclass
class ParsingSet:
    previous_iters_parsed_links: List[str] = field(default_factory=list)
    parser: Optional[AvitoOffersParser] = None
    current_thread_future: Optional[Future] = None
    last_parse_datetime: Optional[datetime.datetime] = None


class Command(BaseCommand):
    """
    Вотчер для отправки подходящих объявлений пользователям.
    Алгоритм:
    1. Берём уникальные пары slug'a города и радиуса поиска, по ним будет строится url для парсера
    2. Для каждой пары создаётся свой объект парсера с уникальным url'ом driver'a
     и запоминается в памяти для оптимизации
    3. Каждый объект парсера помещается в задачу по парсингу страницы и отправке подходящих объявлений юзерам,
        задачи выполняются в потоках для оптимизации

    Парсерам передаются уже обработанные ссылки объявлений для исключения дубликатов сообщений
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.by_slug_by_radius_parsing_set: Dict[str, Dict[int, ParsingSet]] = {}

    def handle(self, *args, **options):
        logger.debug("Start parse_offers")
        AvitoUserOfferWatcher.objects.update(last_checked_offer_datetime=localtime())

        pool = ThreadPoolExecutor()
        try:
            while True:
                slugs_and_search_radius = (
                    AvitoUserOfferWatcher.objects.filter(is_deleted=False)
                    .values("city_url_slug", "search_radius")
                    .distinct("city_url_slug", "search_radius")
                )

                logger.debug(f"Found watchers: {len(slugs_and_search_radius)}")

                for offer_watcher in slugs_and_search_radius.values():
                    sleep(random.randint(0, 20))

                    slug = offer_watcher["city_url_slug"]
                    radius = offer_watcher["search_radius"]

                    parsing_set_by_slug_by_radius = self.by_slug_by_radius_parsing_set.setdefault(slug, {}).get(radius)
                    if not parsing_set_by_slug_by_radius:
                        parsing_set_by_slug_by_radius = ParsingSet()
                        self.by_slug_by_radius_parsing_set.setdefault(slug, {})[radius] = parsing_set_by_slug_by_radius

                    if (
                            parsing_set_by_slug_by_radius.current_thread_future
                    ):
                        if (
                                not parsing_set_by_slug_by_radius.current_thread_future.done()
                                or (
                                    parsing_set_by_slug_by_radius.last_parse_datetime
                                    and localtime() - parsing_set_by_slug_by_radius.last_parse_datetime > settings.PARSE_TIMEOUT_SECONDS
                                    )
                        ):
                            continue
                        else:
                            parsed_links = parsing_set_by_slug_by_radius.current_thread_future.result()
                            logger.debug(
                                f"Task {parsing_set_by_slug_by_radius.current_thread_future} done: {slug} {radius},"
                                f" {parsed_links=}"
                            )
                            parsing_set_by_slug_by_radius.previous_iters_parsed_links.extend(
                                parsed_links
                            )
                    # TODO ПРОВЕРИТЬ ПРАВИЛЬНОСТЬ СРАВНЕНИЯ ПО ВРЕМЕНИ И BUTTON NEXT PAGE
                    if len(parsing_set_by_slug_by_radius.previous_iters_parsed_links) > 200:
                        parsing_set_by_slug_by_radius.previous_iters_parsed_links = (
                            parsing_set_by_slug_by_radius.previous_iters_parsed_links[-200:]
                        )

                    parser = parsing_set_by_slug_by_radius.parser
                    if not parser:
                        parser = AvitoOffersParser(
                                        city_slug=slug,
                                        category_slug="avtomobili",
                                        search_radius=radius
                                    )
                        parsing_set_by_slug_by_radius.parser = parser

                    parses_executor = ParserOffersExecutor(
                        parser=parser,
                        exclude_offers_links=parsing_set_by_slug_by_radius.previous_iters_parsed_links
                    )

                    parsing_set_by_slug_by_radius.current_thread_future = (
                        pool.submit(parses_executor.execute_parse)
                    )
                    logger.debug(f"Publish task {parsing_set_by_slug_by_radius.current_thread_future}: {slug} {radius}")

                time.sleep(random.random() * 20)

        except Exception as e:
            logger.exception(f"Exception while parse: {e}", exc_info=True)
            pool.shutdown()
            self._close_selenium_drivers()

    def _close_selenium_drivers(self) -> None:
        slugs_dicts = self.by_slug_by_radius_parsing_set
        radius_dicts = slugs_dicts.values()
        for radius_dict in radius_dicts:
            parsing_sets = radius_dict.values()
            for parsing_set in parsing_sets:
                if parsing_set.parser:
                    parsing_set.parser.close_driver()
