from avito_parse.models import AvitoCategory, AvitoUserOfferWatcher, AvitoUserOfferWatcherFilter
from avito_parse.filter_forms.transport import FilterFormResult


async def create_avito_offer_watcher(tg_user_id: int, category: AvitoCategory, filter_form_result: FilterFormResult):
    assert (
            len(filter_form_result.validation_recognized_fields_errors) == 0
            and len(filter_form_result.validation_not_recognized_fields_errors) == 0
    )

    filter = await AvitoUserOfferWatcherFilter.objects.acreate(
        specific_filter=filter_form_result.specific_filter
    )

    return await AvitoUserOfferWatcher.objects.acreate(
        telegram_user_id=tg_user_id,
        category=category,
        filter=filter
    )
