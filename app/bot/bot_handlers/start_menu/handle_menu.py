from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery
)

from bot.bot_handlers.constants import (
    MENU_MESSAGE_TEXT,
    CALLBACK_CREATE_OBSERVER, CALLBACK_CREATE_OBSERVER_BUTTON_TEXT,
    CALLBACK_MY_OBSERVERS, CALLBACK_MY_OBSERVERS_BUTTON_TEXT,
    CALLBACK_DONT_SEND_NOTIFICATIONS, CALLBACK_DONT_SEND_NOTIFICATIONS_BUTTON_TEXT,
    CALLBACK_SEND_NOTIFICATIONS, CALLBACK_SEND_NOTIFICATIONS_BUTTON_TEXT
)
from bot.bot import bot
from bot.models import TelegramUser
from bot.services.telegram_user import update_or_create_telegram_user_from_message


async def handle_menu(message: Message):
    await send_menu_as_answer_on_message(message.from_user)


async def send_menu_as_answer_on_message(from_user=None, telegram_user: TelegramUser = None) -> None:
    assert from_user or telegram_user
    if from_user:
        user = await update_or_create_telegram_user_from_message(from_user)
    else:
        user = telegram_user

    buttons = [
        [InlineKeyboardButton(CALLBACK_CREATE_OBSERVER_BUTTON_TEXT, callback_data=CALLBACK_CREATE_OBSERVER)],
        [InlineKeyboardButton(CALLBACK_MY_OBSERVERS_BUTTON_TEXT, callback_data=CALLBACK_MY_OBSERVERS)],
    ]
    if user.need_to_notify:
        buttons.append(
            [
                InlineKeyboardButton(
                    CALLBACK_DONT_SEND_NOTIFICATIONS_BUTTON_TEXT,
                    callback_data=CALLBACK_DONT_SEND_NOTIFICATIONS
                )
            ],
        )
    else:
        buttons.append(
            [
                InlineKeyboardButton(
                    CALLBACK_SEND_NOTIFICATIONS_BUTTON_TEXT,
                    callback_data=CALLBACK_SEND_NOTIFICATIONS
                )
            ],
        )

    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
    await bot.send_message(user.telegram_id, MENU_MESSAGE_TEXT, reply_markup=inline_keyboard)
