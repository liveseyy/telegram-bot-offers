from bot.models import TelegramUser


async def update_or_create_telegram_user_from_message(from_user) -> TelegramUser:
    tg_user, created = await TelegramUser.objects.aupdate_or_create(
        telegram_id=from_user.id,
        defaults={"first_name": from_user.first_name, "username": from_user.username}
    )
    return tg_user
