from aiogram import Dispatcher
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.bot_handlers.start_menu.handle_menu import send_menu_as_answer_on_message


async def handle_unknown_command(message: Message):
    await message.answer("Все функции находятся в меню:")
    await send_menu_as_answer_on_message(message.from_user)


def register_handle_unknown_command(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(handle_unknown_command, lambda message: message)
