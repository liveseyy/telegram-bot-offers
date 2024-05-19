from datetime import datetime
from typing import NamedTuple, Tuple


class ParsedOffer(NamedTuple):
    """
    Данные объявления
    """

    model_brand: str  # "OMODA C5"
    year: int = None  # 2023
    link: str = None  # https://www.avito.ru/ekaterinburg/avtomobili/omoda_c5_1.5_cvt_2023_3942779690
    price: str = None  # 2979900
    show_up_time_ago: str = None  # 3 минуты назад
    show_up_date_time: datetime = None
    city: str = None  # Екатеринбург
    car_parameters: str = None  # 1.5 CVT (147 л.с.), внедорожник, передний, бензин
    mileage: str = None  # "41 000 км"

    @classmethod
    def get_fields_to_fill(cls) -> Tuple[str, ...]:
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
