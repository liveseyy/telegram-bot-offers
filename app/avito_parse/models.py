from django.db import models
from django.utils import timezone

from avito_parse.filter_forms.transport import FilterFormTransport
from bot.models import TelegramUser
from common.models import BaseModel


class AvitoCategory(BaseModel):
    """
    Категории объявлений авито.

    Имеют иерархическую структуру:
    1. Транспорт:
        1.1. Автомобили
        1.2. Мотоциклы и мототехника
            1.2.1 Вездеходы
            ...
        ...
    """
    FITLER_FORM_BASE = "Общая"  # название в объявлениях пишут люди
    # названия в объявлений формирует авито
    FITLER_FORM_TRANSPORT = "Транспорт"

    FILTER_FORM_CLASS_MAP = {
        FITLER_FORM_BASE: FilterFormTransport,
        FITLER_FORM_TRANSPORT: FilterFormTransport
    }

    FILTER_FORM_CHOICES = (
        (FITLER_FORM_BASE, FITLER_FORM_BASE),
        (FITLER_FORM_TRANSPORT, FITLER_FORM_TRANSPORT),
    )

    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(verbose_name="Часть url категории", max_length=150, null=True, unique=True)
    parent_category = models.ForeignKey(
        "self", verbose_name="Родительская категория", null=True, on_delete=models.PROTECT
    )

    filter_form = models.CharField(
        verbose_name="Форма фильтров для парсинга", choices=FILTER_FORM_CHOICES, default=FITLER_FORM_BASE
    )

    @property
    def is_head_category(self) -> bool:
        return self.parent_category is not None


class AvitoUserOfferWatcherFilter(BaseModel):
    """
    Пользовательский фильтр для наблюдателя за объявлениями
    """
    specific_filter = models.JSONField(
        null=True,
        help_text="Фильтры индивидуальные для какой-либо категории, например, пробег авто или кол-во комнат в квартире"
    )


class AvitoUserOfferWatcher(BaseModel):
    """
    Пользовательский наблюдатель за объявлениями
    """
    telegram_user = models.ForeignKey(TelegramUser, verbose_name="Владец вотчера", on_delete=models.PROTECT)
    category = models.ForeignKey(AvitoCategory, verbose_name="Наблюдаемая категория", on_delete=models.PROTECT)
    filter = models.ForeignKey(AvitoUserOfferWatcherFilter, on_delete=models.PROTECT)

    last_checked_offer_datetime = models.DateTimeField(
        default=timezone.localtime, help_text="Пользователю отправляются объявления выложенные после этого времени"
    )
