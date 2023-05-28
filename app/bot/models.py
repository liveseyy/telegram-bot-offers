from django.db import models
from common.models import BaseModel


class TelegramUser(BaseModel):
    """
    Учётка в телеграмме
    """
    telegram_id = models.BigIntegerField(db_index=True, primary_key=True)

    first_name = models.CharField()
    username = models.CharField()
