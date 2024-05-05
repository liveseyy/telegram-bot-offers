from itertools import groupby

from avito_parse.models import AvitoUserOfferWatcher
from common.utils import convert_sync_queryset_to_async


async def get_user_watchers_grouped_by_city(user_telegram_id: int) -> dict:
    user_watchers = await convert_sync_queryset_to_async(
        AvitoUserOfferWatcher.objects.filter(
            telegram_user_id=user_telegram_id,
            is_deleted=False
        )
        .values("id", "city", "search_radius", "filter__specific_filter")
        .order_by("id")
    )
    watcher_grouped_by_city = groupby(user_watchers, lambda d: d["city"])
    return {city: list(watchers) for city, watchers in watcher_grouped_by_city}
