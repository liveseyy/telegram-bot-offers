from aiogram import Bot

from django.conf import settings
"""
Бот отдельно чтобы не было рекурсивных импортов.

Запуск бота проходит в комманде start_bot
"""
bot = Bot(token=settings.TG_BOT_TOKEN)
