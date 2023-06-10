from aiogram import Dispatcher
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery
)

from bot.bot_handlers.constants import (
    MENU_BUTTON_TEXT, MENU_MESSAGE_TEXT,
    CALLBACK_CREATE_OBSERVER, CALLBACK_CREATE_OBSERVER_BUTTON_TEXT,
    CALLBACK_MY_OBSERVERS, CALLBACK_MY_OBSERVERS_BUTTON_TEXT,
    START_COMMAND_GREETING_TEXT,
    CALLBACK_DONT_SEND_NOTIFICATIONS, CALLBACK_DONT_SEND_NOTIFICATIONS_BUTTON_TEXT,
    CALLBACK_SEND_NOTIFICATIONS, CALLBACK_SEND_NOTIFICATIONS_BUTTON_TEXT
)
from bot.services.telegram_user import update_or_create_telegram_user_from_message
from bot.models import TelegramUser
from bot.bot import bot


async def send_menu_as_answer_on_message(user_id: int) -> None:
    user = await TelegramUser.objects.only("need_to_notify").aget(telegram_id=user_id)
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
    await bot.send_message(user_id, MENU_MESSAGE_TEXT, reply_markup=inline_keyboard)


async def handle_start(message: Message):
    await update_or_create_telegram_user_from_message(message=message)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MENU_BUTTON_TEXT)]
        ],
        resize_keyboard=True,
    )

    await message.answer(START_COMMAND_GREETING_TEXT, reply_markup=keyboard)

    await send_menu_as_answer_on_message(user_id=message.from_user.id)


async def handle_menu(message: Message):
    await send_menu_as_answer_on_message(user_id=message.from_user.id)


async def dont_send_notifications(callback_query: CallbackQuery):
    await TelegramUser.objects.aupdate(need_to_notify=False)
    message = (
        "Уведомления об объявлениях теперь вас не потревожат 🔇\n"
        "Возобновить уведомления можно в меню ℹ️"
    )
    await bot.send_message(callback_query.from_user.id, message)
    await send_menu_as_answer_on_message(callback_query.from_user.id)


async def turn_on_send_notifications(callback_query: CallbackQuery):
    await TelegramUser.objects.aupdate(need_to_notify=True)
    message = (
        "Как появится объявление придёт уведомление 🔊\n"
        "Отключить уведомления можно в меню ℹ️"
    )
    await bot.send_message(callback_query.from_user.id, message)
    await send_menu_as_answer_on_message(callback_query.from_user.id)


def register_start_and_menu_on_dispatcher(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(handle_start, commands=["start"])
    dispatcher.register_message_handler(handle_menu, lambda message: message.text == MENU_BUTTON_TEXT)

    dispatcher.register_callback_query_handler(
        dont_send_notifications, lambda c: c.data == CALLBACK_DONT_SEND_NOTIFICATIONS
    )
    dispatcher.register_callback_query_handler(
        turn_on_send_notifications, lambda c: c.data == CALLBACK_SEND_NOTIFICATIONS
    )
