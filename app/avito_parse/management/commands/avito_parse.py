import logging
import time
import traceback

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict

from django.core.management.base import BaseCommand
from django.utils.timezone import localtime

from avito_parse.selenium_parser import AvitoOffersParser
from avito_parse.models import AvitoUserOfferWatcher, AvitoCategory
from avito_parse.services.sync_offers_between_watchers import ParsedOffersBetweenWatchersSync

logger = logging.getLogger("avito_parse")


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

        self.parsed_offer_links_by_previous_iters = []
        # chrome driver'ы для каждой уникальной ссылки, что не открывать драйвер повторно
        self.parser_by_slug_and_search_radius: Dict[str, Dict[int, AvitoOffersParser]] = {}

    def handle(self, *args, **options):
        logger.info("Start avito_parse")
        # AvitoUserOfferWatcher.objects.update(last_checked_offer_datetime=localtime())

        pool = ThreadPoolExecutor(16)
        try:
            while True:
                logger.info("Start avito_parse iteration")

                self._clean_parsed_previous_offers()

                slugs_and_search_radius = (
                    AvitoUserOfferWatcher.objects.filter(is_deleted=False)
                    .values("city_url_slug", "search_radius")
                    .distinct("city_url_slug", "search_radius")
                )

                thread_parse_tasks = []
                for offer_watcher in slugs_and_search_radius.values():
                    slug = offer_watcher["city_url_slug"]
                    radius = offer_watcher["search_radius"]
                    logger.info(f"Publish: {slug} {radius}")

                    parser = self._get_driver_for_parse_by_slug_and_radius(slug=slug, radius=radius)
                    parses_executor = ParsedOffersBetweenWatchersSync(
                        parser=parser,
                        exclude_offers_links=self.parsed_offer_links_by_previous_iters,
                        logger=logger
                    )

                    thread_parse_tasks.append(
                        pool.submit(parses_executor.check_offers_for_watchers)
                    )

                for parse_task_future in as_completed(thread_parse_tasks):
                    parsed_offers_links = parse_task_future.result()
                    logger.info(f"Parsed offers return: {parsed_offers_links}")
                    if parsed_offers_links:
                        self.parsed_offer_links_by_previous_iters.extend(parsed_offers_links)

                time.sleep(1)

        except Exception as e:
            logger.warning(f"Exception while parse: {e}")
            logger.warning(traceback.print_exc())
            pool.shutdown()
            self._close_selenium_drivers()

    def _clean_parsed_previous_offers(self) -> None:
        if len(self.parsed_offer_links_by_previous_iters) > 1000:
            self.parsed_offer_links_by_previous_iters = self.parsed_offer_links_by_previous_iters[-1000:]

    def _close_selenium_drivers(self) -> None:
        dicts_with_radiuses = self.parser_by_slug_and_search_radius.values()
        for parsers_by_radiuses in dicts_with_radiuses:
            drivers = parsers_by_radiuses.values()
            for driver in drivers:
                driver.close_driver()

    def _get_driver_for_parse_by_slug_and_radius(self, slug: str, radius: int) -> AvitoOffersParser:
        parser = self.parser_by_slug_and_search_radius.get(slug, {}).get(radius)
        if not parser:
            parser = AvitoOffersParser(
                city_slug=slug,
                category_slug="avtomobili",
                search_radius=radius
            )
            self.parser_by_slug_and_search_radius.setdefault(slug, dict())[radius] = parser
        return parser
