from datetime import datetime
from typing import NamedTuple, List, Optional, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from avito_parse.common import parse_show_up_time_ago


class AvitoParsedOffer(NamedTuple):
    """
    Данные из объявления авито
    """
    title: str = None
    link: str = None
    price: str = None
    show_up_time_ago: str = None
    show_up_date_time: datetime = None

    @classmethod
    def get_fields_to_fill(cls) -> Tuple[str]:
        return tuple(cls.__annotations__.keys())

    @property
    def easy_to_read_price(self):
        if self.price:
            separated_price = ""
            i = 0
            for digit in reversed(self.price):
                i += 1
                separated_price = digit + separated_price
                if i % 3 == 0:
                    separated_price = " " + separated_price

            separated_price += " ₽"
            return separated_price


class AvitoOffersParser:
    """
    Парсер авито объявлений
    """

    def __init__(self, city_slug: str, category_slug: str, search_radius: int):
        self._driver = None
        self._OFFER_FIELDS_GETTERS_MAP = {
            "title": (
                lambda web_offer_element: web_offer_element.find_element(By.CSS_SELECTOR, "[itemprop='name']").text
            ),
            "link": (
                lambda web_offer_element: (
                    web_offer_element.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").get_attribute("href")
                )
            ),
            "price": (
                lambda web_offer_element: (
                    web_offer_element.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute("content")
                )
            ),
            "show_up_time_ago": self._get_offer_field_show_up_time_ago,
            "show_up_date_time": self._get_offer_field_show_up_date_time
        }

        self._offer_show_up_time_ago = None

        self.avito_url = (
            f"https://www.avito.ru/"
            f"{city_slug}/{category_slug}?"
            f"s=104&"  # сортировка по дате сначала с новых
            f"radius={search_radius}&searchRadius={search_radius}"
        )
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        self._driver = webdriver.Chrome(chrome_options=chrome_options)

    def close_driver(self) -> None:
        self._driver.close()

    def get_parsed_offers(
            self, max_pages: Optional[int] = None, search_before_date: datetime = None
    ) -> List[AvitoParsedOffer]:

        assert max_pages or search_before_date

        self._driver.get(self.avito_url)

        result = []
        current_page = 1
        while True:
            avito_offers = self._driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
            need_break = False
            for offer in avito_offers:
                parsed_offer = self._get_parsed_offer(web_offer_element=offer)
                result.append(parsed_offer)
                print(parsed_offer)
                offer_datetime = parsed_offer.show_up_date_time
                if offer_datetime and search_before_date and offer_datetime < search_before_date:
                    need_break = True
                    break

            if not need_break and self._can_parse_next_page(
                    current_page=current_page, max_pages=max_pages
            ):
                current_page += 1
                continue

            break

        # self._driver.close()

        return result

    def _can_parse_next_page(self, current_page: int, max_pages: Optional[int] = None) -> bool:
        if max_pages is None or current_page < max_pages and self._switch_to_next_page():
            return True

        return False

    def _switch_to_next_page(self) -> bool:
        button_to_next_page = self._driver.find_element(
            By.CSS_SELECTOR, "[data-marker*='pagination-button/next']"
        )
        if button_to_next_page:
            button_to_next_page.click()
            return True

        return False

    def _get_parsed_offer(self, web_offer_element: WebElement) -> AvitoParsedOffer:
        fields_need_to_parse = AvitoParsedOffer.get_fields_to_fill()

        buffer_for_avitor_parsed_offer = {}
        for field_name in fields_need_to_parse:
            buffer_for_avitor_parsed_offer[field_name] = self._OFFER_FIELDS_GETTERS_MAP[field_name](
                web_offer_element=web_offer_element
            )

        return AvitoParsedOffer(**buffer_for_avitor_parsed_offer)

    def _get_offer_field_show_up_time_ago(self, web_offer_element: WebElement) -> str:
        time_web_element = web_offer_element.find_element(By.CSS_SELECTOR, "[data-marker='item-date']")

        show_up_time_ago = time_web_element.text
        self._offer_show_up_time_ago = show_up_time_ago
        return show_up_time_ago

    def _get_offer_field_show_up_date_time(self, web_offer_element: WebElement) -> Optional[datetime]:
        show_up_time_ago_datetime = None
        if self._offer_show_up_time_ago:
            # self._offer_show_up_time_ago = "5 минут назад"
            show_up_time_ago_datetime = parse_show_up_time_ago(show_up_time_ago=self._offer_show_up_time_ago)

        return show_up_time_ago_datetime

    def _get_web_elem_show_up_date_time_verbose(self, web_offer_element: WebElement):
        self._web_elem_show_up_date_time_verbose = web_offer_element.find_element(
            By.CSS_SELECTOR, "[data-placement='bottom']"
        )
        return self._web_elem_show_up_date_time_verbose
