import uuid

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
from django.conf import settings

from bot.bot import bot
from bot.bot_handlers.constants import CALLBACK_CREATE_OBSERVER
from bot.models import TelegramUser
from bot.bot_handlers.start_menu.handle_menu import send_menu_as_answer_on_message

from common.utils import convert_sync_queryset_to_async, method_cache_key
from common.cache_delays import DELAY_1_HOUR
from common.error_messages import ErrorMessageToUser

from avito_parse.models import AvitoCategory
from avito_parse.services.avito_watcher import create_avito_offer_watcher
from avito_parse.services.parse_string import parse_geo_offer_search_settings_from_string

CALLBACK_SELECT_CATEGORY_PREFIX = "SELECT_CATEGORY_"
CALLBACK_CANCEL_SEND_FILTER_FORM = "CALLBACK_CANCEL_SEND_FILTER_FORM"
CALLBACK_CHANGE_GEO_OFFER_SEARCH = "CALLBACK_CHANGE_GEO_OFFER_SEARCH"
CALLBACK_CANCEL_GEO_OFFER_SEARCH = "CALLBACK_CANCEL_GEO_OFFER_SEARCH"


async def create_watcher(callback_query: CallbackQuery):
    """
    Выберите категорию

    заполните форму
    """
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


async def send_request_to_fill_offer_form(selected_category: AvitoCategory, user_id: int):
    filter_form = AvitoCategory.FILTER_FORM_CLASS_MAP[selected_category.filter_form]
    telegram_user = await TelegramUser.objects.aget(telegram_id=user_id)
    cache_key = method_cache_key(
        value_is="session_id",
        user_telegram_id=user_id
    )
    user_session_id = uuid.uuid4()
    cache.set(cache_key, user_session_id, DELAY_1_HOUR)
    form_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    (
                        f"{telegram_user.avito_city}, +{telegram_user.avito_search_radius}км 🌎 ⚙️"
                    ),
                    callback_data=CALLBACK_CHANGE_GEO_OFFER_SEARCH
                )
            ],
            [InlineKeyboardButton("Заполнить форму по ссылке 🌐 ⚙️",
                                  url=(
                                      f"{settings.WEB_DOMAIN}/"
                                      f"{settings.OFFERS_CAR_WATCHER_FORM_CREATE_URL_PREFIX}"
                                      f"?user_id={user_id}&session_id={user_session_id}"
                                  ))],
            [InlineKeyboardButton("Отменить создание наблюдения 📢 ❌", callback_data=CALLBACK_CANCEL_SEND_FILTER_FORM)]
        ],
    )
    # отправляём пользователю форму и запоминаем его состояние в кэше
    await bot.send_message(
        user_id, filter_form.get_formatted_message(user_id=user_id), parse_mode="HTML", reply_markup=form_keyboard
    )
    cache_key = method_cache_key(cache_prefix="create_observer", method="handle_selected_category",
                                 user_telegram_id=user_id)
    cache.set(cache_key, selected_category, DELAY_1_HOUR)


async def handle_selected_category(callback_query: CallbackQuery):
    selected_category_id = callback_query.data.replace(CALLBACK_SELECT_CATEGORY_PREFIX, "")

    try:
        selected_category = await AvitoCategory.objects.aget(id=selected_category_id)
        await send_request_to_fill_offer_form(
            selected_category=selected_category,
            user_id=callback_query.from_user.id
        )

    except ObjectDoesNotExist:
        await bot.send_message(callback_query.from_user.id, "Такой категории нет ❌")


def delete_cache_stage_create_watcher(user_telegram_id):
    cache_key = method_cache_key(cache_prefix="create_observer", method="handle_selected_category",
                                 user_telegram_id=user_telegram_id)
    cache.delete(cache_key)


async def cancel_create_watcher(callback_query: CallbackQuery):
    delete_cache_stage_create_watcher(callback_query.from_user.id)

    message_to_user = "Создание объявления отменено ❌\n" \
                      "Вы можете повторить создания через меню:"
    await bot.send_message(
        callback_query.from_user.id, message_to_user
    )
    await send_menu_as_answer_on_message(callback_query.from_user)


async def change_geo_offer_search(callback_query: CallbackQuery):
    message_to_user = (
        "Напишите название города и радиус поиска в километрах через запятую (регистр букв не важен)\n\n"
        "Примеры (копируются при нажатии):\n"
        "<code>Челябинск, 124</code>\n"
        "<code>Москва,200</code>\n"
        "<code>гусь-хрустальный,300</code>\n"
        "<code>павловский посад  ,  250</code>\n"
        "<code>славянск-на-кубани ,250</code>\n"
    )

    form_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Отменить изменение гео. поиска 🌎 ❌",
                                     callback_data=CALLBACK_CANCEL_GEO_OFFER_SEARCH)
            ]
        ],
    )

    cache_key = method_cache_key(on_stage="change_geo_offer_search",
                                 next_stage="handle_change_geo_offer_search",
                                 user_telegram_id=callback_query.from_user.id)
    cache.set(cache_key, True)

    await bot.send_message(
        callback_query.from_user.id, message_to_user, reply_markup=form_keyboard,
        parse_mode="HTML"
    )


async def cancel_geo_offer_search(callback_query: CallbackQuery):
    cache_key = method_cache_key(on_stage="change_geo_offer_search",
                                 next_stage="handle_change_geo_offer_search",
                                 user_telegram_id=callback_query.from_user.id)
    cache.delete(cache_key)
    message_to_user = "Изменение геолокации поиска отменено 🌎 ❌"
    await bot.send_message(
        callback_query.from_user.id, message_to_user
    )
    cache_key = method_cache_key(cache_prefix="create_observer", method="handle_selected_category",
                                 user_telegram_id=callback_query.from_user.id)
    selected_category = cache.get(cache_key)
    if selected_category:
        await send_request_to_fill_offer_form(selected_category=selected_category, user_id=callback_query.from_user.id)


def stage_is_handle_change_geo_offer_search(user_id: int) -> bool:
    cache_key = method_cache_key(on_stage="change_geo_offer_search",
                                 next_stage="handle_change_geo_offer_search",
                                 user_telegram_id=user_id)
    return cache.get(cache_key)


async def handle_change_geo_offer_search(message: Message) -> None:
    user_id = message.from_user.id

    offer_search_settings_result = parse_geo_offer_search_settings_from_string(message.text)

    if isinstance(offer_search_settings_result, ErrorMessageToUser):
        await bot.send_message(user_id, offer_search_settings_result.message)
        return

    await TelegramUser.objects.aupdate(
        avito_city_url_slug=offer_search_settings_result.city_url_slug,
        avito_city=offer_search_settings_result.city,
        avito_search_radius=offer_search_settings_result.radius_search,
    )

    cache_key = method_cache_key(on_stage="change_geo_offer_search",
                                 next_stage="handle_change_geo_offer_search",
                                 user_telegram_id=user_id)
    cache.delete(cache_key)

    await bot.send_message(user_id, "Геолокация поиска изменена ✅ 🌎")

    cache_key = method_cache_key(cache_prefix="create_observer", method="handle_selected_category",
                                 user_telegram_id=message.from_user.id)
    selected_category = cache.get(cache_key)
    if selected_category:
        await send_request_to_fill_offer_form(selected_category=selected_category, user_id=user_id)


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
            await send_menu_as_answer_on_message(message.from_user)


def register_create_observer_on_dispatcher(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(create_watcher, lambda c: c.data == CALLBACK_CREATE_OBSERVER)
    dispatcher.register_callback_query_handler(handle_selected_category, filters.Regexp(regexp="^SELECT_CATEGORY_\d+$"))

    dispatcher.register_callback_query_handler(cancel_create_watcher,
                                               lambda c: c.data == CALLBACK_CANCEL_SEND_FILTER_FORM)
    dispatcher.register_callback_query_handler(change_geo_offer_search,
                                               lambda c: c.data == CALLBACK_CHANGE_GEO_OFFER_SEARCH)
    dispatcher.register_callback_query_handler(cancel_geo_offer_search,
                                               lambda c: c.data == CALLBACK_CANCEL_GEO_OFFER_SEARCH)

    dispatcher.register_message_handler(
        handle_change_geo_offer_search, lambda m: stage_is_handle_change_geo_offer_search(m.from_user.id)
    )

    dispatcher.register_message_handler(
        handle_user_filter_form_selected_category, lambda m: get_selected_user_category_from_cache(m.from_user.id)
    )
