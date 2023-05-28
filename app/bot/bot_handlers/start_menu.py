from aiogram import Dispatcher
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.bot_handlers.constants import (
    MENU_BUTTON_TEXT, MENU_MESSAGE_TEXT,
    CALLBACK_CREATE_OBSERVER, CALLBACK_CREATE_OBSERVER_BUTTON_TEXT,
    CALLBACK_MY_OBSERVERS, CALLBACK_MY_OBSERVERS_BUTTON_TEXT,
    START_COMMAND_GREETING_TEXT
)
from bot.services.telegram_user import update_or_create_telegram_user_from_message


async def send_menu_as_answer_on_message(message: Message) -> None:
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(CALLBACK_CREATE_OBSERVER_BUTTON_TEXT, callback_data=CALLBACK_CREATE_OBSERVER)],
            [InlineKeyboardButton(CALLBACK_MY_OBSERVERS_BUTTON_TEXT, callback_data=CALLBACK_MY_OBSERVERS)],
        ]
    )
    await message.answer(MENU_MESSAGE_TEXT, reply_markup=inline_keyboard)


async def handle_start(message: Message):
    await update_or_create_telegram_user_from_message(message=message)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MENU_BUTTON_TEXT)]
        ],
        resize_keyboard=True,
    )

    await message.answer(START_COMMAND_GREETING_TEXT, reply_markup=keyboard)

    await send_menu_as_answer_on_message(message=message)


async def handle_menu(message: Message):
    await send_menu_as_answer_on_message(message=message)


def register_start_and_menu_on_dispatcher(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(handle_start, commands=["start"])
    dispatcher.register_message_handler(handle_menu, lambda message: message.text == MENU_BUTTON_TEXT)
