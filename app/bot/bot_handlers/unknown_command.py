from aiogram import Dispatcher
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.bot_handlers.start_menu import send_menu_as_answer_on_message


async def handle_unknown_command(message: Message):
    await message.answer("Все функции находятся в меню:")
    await send_menu_as_answer_on_message(user_id=message.from_user.id)


def register_handle_unknown_command(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(handle_unknown_command, lambda message: message)
