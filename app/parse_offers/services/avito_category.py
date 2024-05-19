from parse_offers.models import AvitoCategory


async def get_avito_car_category():
    return await AvitoCategory.objects.aget(slug="avtomobili")


def get_avito_category_filter_form(avito_category: AvitoCategory):
    return AvitoCategory.FILTER_FORM_CLASS_MAP[avito_category.filter_form]
