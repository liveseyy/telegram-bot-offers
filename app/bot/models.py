from django.db import models
from common.models import BaseModel

from parse_offers.geo_offer_search_settings import (
    RU_CITIES_URL_SLUGS_CHOICES, RU_CITIES_CHOICES,
    DEFAULT_CITY_URL_SLUG, DEFAULT_CITY,
    DEFAULT_SEARCH_RADIUS
)


class TelegramUser(BaseModel):
    """
    Учётка в телеграмме
    """
    telegram_id = models.BigIntegerField(db_index=True, primary_key=True)

    first_name = models.CharField()
    username = models.CharField()

    need_to_notify = models.BooleanField(verbose_name="Уведомлять об объявлениях", default=True)

    avito_city_url_slug = models.CharField(max_length=100, choices=RU_CITIES_URL_SLUGS_CHOICES,
                                           default=DEFAULT_CITY_URL_SLUG)
    avito_city = models.CharField(max_length=200, choices=RU_CITIES_CHOICES, default=DEFAULT_CITY)
    avito_search_radius = models.PositiveSmallIntegerField(default=DEFAULT_SEARCH_RADIUS)
