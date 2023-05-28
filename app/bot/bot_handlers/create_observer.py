from aiogram import Dispatcher
from aiogram.dispatcher import filters
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message
)
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

from bot.bot import bot
from bot.bot_handlers.constants import CALLBACK_CREATE_OBSERVER
from common.utils import convert_sync_queryset_to_async, convert_sync_func_to_async, method_cache_key
from common.cache_delays import DELAY_1_HOUR
from avito_parse.models import AvitoCategory
from avito_parse.services.avito_watcher import create_avito_offer_watcher


CALLBACK_SELECT_CATEGORY_PREFIX = "SELECT_CATEGORY_"
CALLBACK_CANCEL_SEND_FILTER_FORM = "CALLBACK_CANCEL_SEND_FILTER_FORM"


async def create_watcher(callback_query: CallbackQuery):
    """
    Выберите категорию

    заполните форму
    """
    # get categories inline buttons
    categories = await convert_sync_queryset_to_async(
        AvitoCategory.objects.all()
    )
    message_to_select_category = "Выберите категорию объявления:"
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(category.title, callback_data=f"{CALLBACK_SELECT_CATEGORY_PREFIX}{category.id}")]
            for category in categories
        ]
    )

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, message_to_select_category, reply_markup=inline_keyboard)


async def handle_selected_category(callback_query: CallbackQuery):
    selected_category_id = callback_query.data.replace(CALLBACK_SELECT_CATEGORY_PREFIX, "")

    try:
        selected_category = await AvitoCategory.objects.aget(id=selected_category_id)
        filter_form = AvitoCategory.FILTER_FORM_CLASS_MAP[selected_category.filter_form]
        cancel_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Отменить создание наблюдения ❌", callback_data=CALLBACK_CANCEL_SEND_FILTER_FORM)]
            ]
        )
        # отправляём пользователю форму и запоминаем его состояние в кэше
        await bot.send_message(
            callback_query.from_user.id, filter_form.MESSAGE, parse_mode="MarkDown", reply_markup=cancel_keyboard
        )
        cache_key = method_cache_key(cache_prefix="create_observer", method="handle_selected_category",
                                     user_telegram_id=callback_query.from_user.id)
        cache.set(cache_key, selected_category, DELAY_1_HOUR)

    except ObjectDoesNotExist:
        await bot.send_message(callback_query.from_user.id, "Такой категории нет")


async def cancel_create_watcher(callback_query: CallbackQuery):
    cache_key = method_cache_key(cache_prefix="create_observer", method="handle_selected_category",
                                 user_telegram_id=callback_query.from_user.id)
    cache.delete(cache_key)

    message_to_user = "Создание объявления отменено.\n" \
                      "Вы можете повторить создания через меню"
    await bot.send_message(
        callback_query.from_user.id, message_to_user, parse_mode="MarkDown"
    )


def get_selected_user_category_from_cache(user_id: int):
    cache_key = method_cache_key(cache_prefix="create_observer", method="handle_selected_category",
                                 user_telegram_id=user_id)
    return cache.get(cache_key)


async def handle_user_filter_form_selected_category(message: Message) -> None:
    tg_user_id = message.from_user.id
    selected_category = get_selected_user_category_from_cache(tg_user_id)

    if selected_category:
        filter_form = AvitoCategory.FILTER_FORM_CLASS_MAP[selected_category.filter_form]
        filter_form_result = filter_form.process_user_filter_form(text=message.text)
        if (
                filter_form_result.validation_not_recognized_fields_errors
                or filter_form_result.validation_recognized_fields_errors
        ):
            validation_errors_message = ""

            if filter_form_result.validation_not_recognized_fields_errors:
                bad_rows = filter_form_result.validation_not_recognized_fields_errors
                validation_errors_message = "Неправильный формат полей:\n"
                for row in bad_rows:
                    validation_errors_message += f"{row} ❌\n"
                validation_errors_message += "\n"

            if filter_form_result.validation_recognized_fields_errors:
                bad_rows = filter_form_result.validation_recognized_fields_errors
                validation_errors_message += "Неправильное значение полей:\n"
                for row in bad_rows:
                    validation_errors_message += f"{row} ❌\n"

            await bot.send_message(
                tg_user_id, validation_errors_message
            )
        else:
            await create_avito_offer_watcher(
                tg_user_id=tg_user_id,
                category=selected_category,
                filter_form_result=filter_form_result
            )
            await bot.send_message(
                tg_user_id, "Наблюдение создано ✅"
            )
            cache_key = method_cache_key(cache_prefix="create_observer",
                                         method="handle_selected_category",
                                         user_telegram_id=tg_user_id)
            cache.delete(cache_key)


def register_create_observer_on_dispatcher(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(create_watcher, lambda c: c.data == CALLBACK_CREATE_OBSERVER)
    dispatcher.register_callback_query_handler(handle_selected_category, filters.Regexp(regexp="^SELECT_CATEGORY_\d+$"))

    dispatcher.register_callback_query_handler(cancel_create_watcher, lambda c: c.data == CALLBACK_CANCEL_SEND_FILTER_FORM)

    dispatcher.register_message_handler(
        handle_user_filter_form_selected_category, lambda m: get_selected_user_category_from_cache(m.from_user.id)
    )
