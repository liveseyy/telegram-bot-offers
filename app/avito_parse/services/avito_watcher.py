from avito_parse.models import AvitoCategory, AvitoUserOfferWatcher, AvitoUserOfferWatcherFilter
from bot.models import TelegramUser
from avito_parse.filter_forms.transport import FilterFormResult
from avito_parse.geo_offer_search_settings import RU_CITIES_URL_SLUGS


async def create_avito_offer_watcher(tg_user_id: int, category: AvitoCategory, filter_form_result: FilterFormResult):
    assert (
            len(filter_form_result.validation_recognized_fields_errors) == 0
            and len(filter_form_result.validation_not_recognized_fields_errors) == 0
    )

    filter = await AvitoUserOfferWatcherFilter.objects.acreate(
        specific_filter=filter_form_result.specific_filter
    )
    telegram_user = await TelegramUser.objects.aget(telegram_id=tg_user_id)

    return await AvitoUserOfferWatcher.objects.acreate(
        telegram_user_id=tg_user_id,
        category=category,
        filter=filter,
        city_url_slug=RU_CITIES_URL_SLUGS[telegram_user.avito_city],
        city=telegram_user.avito_city,
        search_radius=telegram_user.avito_search_radius
    )
