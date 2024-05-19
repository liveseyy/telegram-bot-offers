from typing import Iterable

from common.utils import convert_sync_queryset_to_async
from parse_offers.models import AvitoUserOfferWatcher, AvitoCategory


async def get_message_with_user_watchers(telegram_user_id: int) -> str:
    user_watchers = await convert_sync_queryset_to_async(
        AvitoUserOfferWatcher.objects.filter(
            telegram_user_id=telegram_user_id,
            is_deleted=False
        )
        .select_related("category", "filter")
        .order_by("id")
    )

    if not user_watchers:
        return "Нет наблюдений"

    formatted_message = "Ваши наблюдения 👁\n(текст копируется при нажатии)\n"
    user_offers_group_by_categories = {}
    for user_watcher in user_watchers:
        user_offers_group_by_categories.setdefault(user_watcher.category.title, []).append(user_watcher)

    for category_title, watchers in user_offers_group_by_categories.items():
        formatted_message += f"\n{category_title}\n"
        formatted_message += get_numbered_verbose_watchers(watchers=watchers)

    return formatted_message


def get_numbered_verbose_watchers(watchers: Iterable[AvitoUserOfferWatcher]) -> str:
    numbered_string_watchers = ""
    number_of_watcher = 1
    for watcher in watchers:
        filter_form_service = AvitoCategory.FILTER_FORM_CLASS_MAP[watcher.category.filter_form]
        offer_filter_verbose = (
            filter_form_service.format_specific_filter_to_verbose_name(
                specific_filter=watcher.filter.specific_filter
            )
        )
        numbered_string_watchers += f"{number_of_watcher}. {watcher.city}, +{watcher.search_radius}км 🌎\n"
        numbered_string_watchers += f"Идентификатор: <code>{watcher.id}</code>\n"
        numbered_string_watchers += f"<code>{offer_filter_verbose}</code>\n\n"

        number_of_watcher += 1

    return numbered_string_watchers
