from aiogram.types import Message
from bot.models import TelegramUser


async def update_or_create_telegram_user_from_message(message: Message) -> None:
    dialog_user = message.from_user

    await TelegramUser.objects.aupdate_or_create(
        telegram_id=dialog_user.id,
        defaults={"first_name": dialog_user.first_name, "username": dialog_user.username}
    )
