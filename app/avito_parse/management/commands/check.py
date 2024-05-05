from datetime import datetime
from typing import NamedTuple, List, Optional, Tuple


class AvitoParsedOffer(NamedTuple):
    """
    Данные из объявления авито
    """
    title: str = None
    link: str = None
    price: str = None
    show_up_time_ago: str = None
    show_up_date_time: datetime = None
    city: str = None
    car_parameters: str = None
    mileage: str = None # 41 000 км

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
            separated_price = separated_price.strip()
            return separated_price
