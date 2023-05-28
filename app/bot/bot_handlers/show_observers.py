from typing import Optional, List, Set

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message

from django.core.cache import cache

from common.utils import convert_sync_queryset_to_async, method_cache_key
from common.cache_delays import DELAY_1_HOUR

from avito_parse.models import AvitoUserOfferWatcher

from bot.bot import bot
from bot.services.avito_watchers import get_message_with_user_watchers, get_numbered_verbose_watchers
from bot.bot_handlers.constants import CALLBACK_MY_OBSERVERS, CALLBACK_MY_OBSERVERS_BUTTON_TEXT, MENU_BUTTON_TEXT

CALLBACK_DELETE_WATCHERS = "CALLBACK_DELETE_WATCHERS"
CALLBACK_CANCEL_DELETE_WATCHERS = "CALLBACK_CANCEL_DELETE_WATCHERS"
CALLBACK_ACCESS_DELETE_WATCHERS = "CALLBACK_ACCESS_DELETE_WATCHERS"
CALLBACK_RETRY_DELETE_WATCHERS = "CALLBACK_RETRY_DELETE_WATCHERS"


def user_is_deletes_watchers(user_id: int) -> Optional[bool]:
    cache_key = method_cache_key(cache_prefix="show_observers", method="delete_watchers",
                                 user_telegram_id=user_id)
    return cache.get(cache_key)


def get_user_watchers_ids_to_delete(user_id: int) -> Optional[Set[AvitoUserOfferWatcher]]:
    cache_key = method_cache_key(cache_prefix="show_observers",
                                 method="handle_delete_watchers_ids",
                                 stage="delete_on_accessing",
                                 user_telegram_id=user_id)
    return cache.get(cache_key)


async def show_my_watchers(callback_query: CallbackQuery):
    message_to_user = await get_message_with_user_watchers(telegram_user_id=callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)

    if message_to_user == "Нет наблюдений":
        await bot.send_message(callback_query.from_user.id, message_to_user)
    else:
        inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Выбрать наблюдения для удаления 🗑", callback_data=CALLBACK_DELETE_WATCHERS)],
            ]
        )
        await bot.send_message(callback_query.from_user.id, message_to_user,
                               reply_markup=inline_keyboard, parse_mode="MarkDown")


async def delete_watchers(callback_query: CallbackQuery):
    cache_key = method_cache_key(cache_prefix="show_observers", method="delete_watchers",
                                 user_telegram_id=callback_query.from_user.id)
    cache.set(cache_key, True, DELAY_1_HOUR)

    await bot.answer_callback_query(callback_query.id)

    instruction_to_delete = (
        "Чтобы удалить наблюдения отправьте идентификаторы через пробел.\n\n"
        f"Идентификаторы можно получить пройдя в меню по пути:\n"
        f"_{MENU_BUTTON_TEXT}"
        f"\n            ⬇️\n"
        f"{CALLBACK_MY_OBSERVERS_BUTTON_TEXT}_"
        f"\n\n"
        f"Отправку идентификаторов можно отменить нажав кнопку (отменится автоматически через 1 час):"
    )
    cancel_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Отменить удаление наблюдений ❌", callback_data=CALLBACK_CANCEL_DELETE_WATCHERS)]
        ]
    )
    await bot.send_message(callback_query.from_user.id, instruction_to_delete,
                           reply_markup=cancel_keyboard, parse_mode="MarkDown")


async def cancel_delete_watchers(callback_query: CallbackQuery):
    cache_key = method_cache_key(cache_prefix="show_observers", method="delete_watchers",
                                 user_telegram_id=callback_query.from_user.id)
    cache.delete(cache_key)

    message_to_user = "Удаление наблюдений отменено ✅"
    await bot.send_message(
        callback_query.from_user.id, message_to_user
    )


async def handle_delete_watchers_ids(message: Message) -> None:
    tg_user_id = message.from_user.id
    is_delete_stage = user_is_deletes_watchers(tg_user_id)

    if is_delete_stage:
        watchers_raw_ids = message.text.split()
        watchers_ids = filter(lambda s: s.isdigit(), watchers_raw_ids)
        found_watchers_by_ids = await convert_sync_queryset_to_async(
            AvitoUserOfferWatcher.objects.filter(
                telegram_user_id=tg_user_id,
                id__in=watchers_ids,
                is_deleted=False
            )
            .select_related("category", "filter")
            .order_by("id")
        )
        found_watchers_by_ids_ids = set(map(lambda x: str(x.id), found_watchers_by_ids))
        no_found_ids = set(watchers_raw_ids).difference(found_watchers_by_ids_ids)
        if no_found_ids:
            await bot.send_message(
                tg_user_id, f"Идентификаторы не найдены: {', '.join(no_found_ids)} ❌"
            )
        else:
            numbered_verbose_watchers = get_numbered_verbose_watchers(watchers=found_watchers_by_ids)
            inline_access_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton("Да ✅", callback_data=CALLBACK_ACCESS_DELETE_WATCHERS),
                        InlineKeyboardButton("Нет ❌", callback_data=CALLBACK_RETRY_DELETE_WATCHERS)
                    ],
                ]
            )
            cache_key = method_cache_key(cache_prefix="show_observers",
                                         method="handle_delete_watchers_ids",
                                         stage="delete_on_accessing",
                                         user_telegram_id=tg_user_id)
            cache.set(cache_key, found_watchers_by_ids_ids, DELAY_1_HOUR)
            await bot.send_message(
                tg_user_id,
                f"Вы уверены что хотите удалить эти наблюдения? 🗑\n\n{numbered_verbose_watchers}",
                reply_markup=inline_access_keyboard,
                parse_mode="MarkDown"
            )


async def access_delete_watchers(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    watchers_ids = get_user_watchers_ids_to_delete(user_id=user_id)
    if watchers_ids:
        await AvitoUserOfferWatcher.objects.filter(id__in=watchers_ids).aupdate(is_deleted=True)
        cache_key_stage_delete = method_cache_key(cache_prefix="show_observers", method="delete_watchers",
                                     user_telegram_id=user_id)
        cache_key_stage_accessing_delete = method_cache_key(cache_prefix="show_observers",
                                     method="handle_delete_watchers_ids",
                                     stage="delete_on_accessing",
                                     user_telegram_id=user_id)
        cache.delete(cache_key_stage_delete)
        cache.delete(cache_key_stage_accessing_delete)
        await bot.send_message(
            user_id, "Наблюдения удалены ✅"
        )
    else:
        await bot.send_message(
            user_id, "Невозможно удалить наблюдения, попробуйте сначала"
        )


async def retry_delete_watchers(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    cache_key_stage_accessing_delete = method_cache_key(cache_prefix="show_observers",
                                                        method="handle_delete_watchers_ids",
                                                        stage="delete_on_accessing",
                                                        user_telegram_id=user_id)
    cache.delete(cache_key_stage_accessing_delete)
    await bot.send_message(
        user_id, "Удаление выбранных наблюдений отменено\n"
    )


def register_show_my_observers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(show_my_watchers, lambda c: c.data == CALLBACK_MY_OBSERVERS)
    dispatcher.register_callback_query_handler(delete_watchers, lambda c: c.data == CALLBACK_DELETE_WATCHERS)
    dispatcher.register_callback_query_handler(
        cancel_delete_watchers, lambda c: c.data == CALLBACK_CANCEL_DELETE_WATCHERS
    )

    dispatcher.register_message_handler(
        handle_delete_watchers_ids, lambda m: user_is_deletes_watchers(m.from_user.id)
    )

    dispatcher.register_callback_query_handler(
        access_delete_watchers, lambda c: c.data == CALLBACK_ACCESS_DELETE_WATCHERS
    )
    dispatcher.register_callback_query_handler(
        retry_delete_watchers, lambda c: c.data == CALLBACK_RETRY_DELETE_WATCHERS
    )
