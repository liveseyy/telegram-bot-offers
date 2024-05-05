from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery
)

from bot.bot_handlers.start_menu.handle_menu import send_menu_as_answer_on_message
from bot.models import TelegramUser
from bot.bot import bot


async def handle_dont_send_notifications(callback_query: CallbackQuery):
    await TelegramUser.objects.aupdate(need_to_notify=False)
    message = (
        "Уведомления об объявлениях теперь вас не потревожат 🔇\n"
        "Возобновить уведомления можно в меню ℹ️"
    )
    await bot.send_message(callback_query.from_user.id, message)
    await send_menu_as_answer_on_message(callback_query.from_user)


async def handle_turn_on_send_notifications(callback_query: CallbackQuery):
    await TelegramUser.objects.aupdate(need_to_notify=True)
    message = (
        "Как появится объявление придёт уведомление 🔊\n"
        "Отключить уведомления можно в меню ℹ️"
    )
    await bot.send_message(callback_query.from_user.id, message)
    await send_menu_as_answer_on_message(callback_query.from_user)
