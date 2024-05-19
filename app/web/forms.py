import re

from typing import Optional

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from parse_offers.geo_offer_search_settings import RU_CITIES_CHOICES, DEFAULT_CITY
from parse_offers.avito_cars_brands_models import BRANDS_MODELS_CHOICES
from parse_offers.services.avito_watcher import create_avito_offer_watcher
from parse_offers.services.avito_category import get_avito_car_category, get_avito_category_filter_form

from bot.models import TelegramUser


class OfferWatchersForm(forms.Form):
    MIN_YEAR_VALUE = 1960
    MAX_YEAR_VALUE = timezone.localdate().year

    city = forms.ChoiceField(label="Город", choices=RU_CITIES_CHOICES, initial=DEFAULT_CITY)

    radius_search = forms.IntegerField(label="Радиус поиска", min_value=1, max_value=3000)

    brand_model = forms.ChoiceField(label="Марка, модель", choices=BRANDS_MODELS_CHOICES)

    price_from = forms.CharField(label="Цена, от", required=False)
    price_to = forms.CharField(label="Цена, до", required=False)

    year_from = forms.CharField(label=f"Год, от {MIN_YEAR_VALUE}", required=False)
    year_to = forms.CharField(label=f"Год, до {MAX_YEAR_VALUE}", required=False)

    mileage_from = forms.CharField(label="Пробег, от", required=False)
    mileage_to = forms.CharField(label="Пробег, до", required=False)

    POSITIVE_VALIDATION_ERROR_TEXT = "Число должно быть неотрицательным"
    YEAR_VALIDATION_ERROR_TEXT = f"Год должен быть в рамках от {MIN_YEAR_VALUE} до {MAX_YEAR_VALUE}"

    MAX_MILEAGE = 10_000_000
    VERBOSE_MAX_MILEAGE = "10 000 000"
    MILEAGE_MAX_VALIDATION_ERROR_TEXT = f"Максимальное значение {VERBOSE_MAX_MILEAGE} км"

    def __init__(self, *args, tg_user: TelegramUser, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["city"].initial = tg_user.avito_city
        self.fields["radius_search"].initial = tg_user.avito_search_radius

        self.tg_user = tg_user

    @staticmethod
    def _get_digits_string_from_value(value: str):
        """
        строка число с минусом или без
        """
        if not value:
            return value

        if value[0] == "-":
            return "-" + re.sub("(\D)|(-)", "", value)
        return re.sub("(\D)|(-)", "", value)

    def _validate_integer_value(self, field_name: str, return_null=True):
        digits_string = self._get_digits_string_from_value(self.cleaned_data[field_name])
        if return_null and not digits_string:
            return

        try:
            return int(digits_string)
        except ValueError:
            raise ValidationError("Значение должно быть числом")

    def _validate_positive_integer_field(self, value):
        if value is not None and value < 0:
            raise ValidationError(self.POSITIVE_VALIDATION_ERROR_TEXT)

    def _validate_year_field(self, year):
        if year is not None and (year < self.MIN_YEAR_VALUE or year > self.MAX_YEAR_VALUE):
            raise ValidationError(self.YEAR_VALIDATION_ERROR_TEXT)

    def clean_price_from(self):
        price_from = self._validate_integer_value(field_name="price_from", return_null=True)
        self._validate_positive_integer_field(price_from)
        return price_from

    def clean_price_to(self):
        price_to = self._validate_integer_value(field_name="price_to", return_null=True)
        self._validate_positive_integer_field(price_to)

        price_from = self.cleaned_data.get("price_from")
        if price_to is not None and price_from is not None and price_from > price_to:
            raise ValidationError('Цена должна быть больше или равна "Цена, от"')
        return price_to

    def clean_year_from(self):
        year_from = self._validate_integer_value(field_name="year_from", return_null=True)
        self._validate_positive_integer_field(year_from)
        self._validate_year_field(year_from)
        return year_from

    def clean_year_to(self):
        year_to = self._validate_integer_value(field_name="year_to", return_null=True)
        self._validate_positive_integer_field(year_to)
        self._validate_year_field(year_to)

        year_from = self.cleaned_data.get("year_from")
        if year_to is not None and year_from is not None and year_from > year_to:
            raise ValidationError('Год должен быть больше или равен "Год, от"')
        return year_to

    def _validate_max_mileage(self, mileage: Optional[int]):
        if mileage is not None and mileage > self.MAX_MILEAGE:
            raise ValidationError(self.MILEAGE_MAX_VALIDATION_ERROR_TEXT)

    def clean_mileage_from(self):
        mileage_from = self._validate_integer_value(field_name="mileage_from", return_null=True)
        self._validate_positive_integer_field(mileage_from)
        self._validate_max_mileage(mileage_from)
        return mileage_from

    def clean_mileage_to(self):
        mileage_to = self._validate_integer_value(field_name="mileage_to", return_null=True)
        self._validate_positive_integer_field(mileage_to)
        self._validate_max_mileage(mileage_to)

        mileage_from = self.cleaned_data.get("mileage_from")
        if mileage_to is not None and mileage_from is not None and mileage_from > mileage_to:
            raise ValidationError('Пробег должен быть больше или равен "Пробег, от"')
        return mileage_to

    async def update_user_city_and_radius(self):
        form_city = self.cleaned_data["city"]
        form_radius_search = self.cleaned_data["radius_search"]

        need_update = False
        if self.tg_user.avito_city != form_city:
            self.tg_user.avito_city = form_city
            need_update = True
        if self.tg_user.avito_search_radius != form_radius_search:
            self.tg_user.avito_search_radius = form_radius_search
            need_update = True

        if need_update:
            await self.tg_user.asave(update_fields=["avito_city", "avito_search_radius"])

    async def create_offer_watcher(self):
        selected_category = await get_avito_car_category()
        filter_form = get_avito_category_filter_form(selected_category)
        filter_form_result = filter_form.process_user_filter_web_form(data=self.cleaned_data)
        await create_avito_offer_watcher(
            tg_user_id=self.tg_user.telegram_id,
            category=selected_category,
            filter_form_result=filter_form_result
        )
