from aiogram import Dispatcher

from bot.bot_handlers.constants import (
    MENU_BUTTON_TEXT,
    CALLBACK_DONT_SEND_NOTIFICATIONS,
    CALLBACK_SEND_NOTIFICATIONS
)

from bot.bot_handlers.start_menu.handle_start import handle_start
from bot.bot_handlers.start_menu.handle_menu import handle_menu
from bot.bot_handlers.start_menu.handle_notify_flag import (
    handle_turn_on_send_notifications, handle_dont_send_notifications
)


def register_start_and_menu_on_dispatcher(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(handle_start, commands=["start"])
    dispatcher.register_message_handler(handle_menu, lambda message: message.text == MENU_BUTTON_TEXT)

    dispatcher.register_callback_query_handler(
        handle_dont_send_notifications, lambda c: c.data == CALLBACK_DONT_SEND_NOTIFICATIONS
    )
    dispatcher.register_callback_query_handler(
        handle_dont_send_notifications, lambda c: c.data == CALLBACK_SEND_NOTIFICATIONS
    )
