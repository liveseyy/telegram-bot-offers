from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery
)


from bot.bot_handlers.start_menu.handle_menu import send_menu_as_answer_on_message
from bot.bot_handlers.constants import MENU_BUTTON_TEXT, START_COMMAND_GREETING_TEXT
from bot.services.telegram_user import update_or_create_telegram_user_from_message


async def handle_start(message: Message):
    await update_or_create_telegram_user_from_message(message.from_user)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MENU_BUTTON_TEXT)]
        ],
        resize_keyboard=True,
    )

    await message.answer(START_COMMAND_GREETING_TEXT, reply_markup=keyboard)

    await send_menu_as_answer_on_message(message.from_user)
