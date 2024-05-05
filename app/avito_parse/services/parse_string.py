from typing import Union

from common.error_messages import ErrorMessageToUser
from avito_parse.geo_offer_search_settings import GeoOfferSearchSettings, RU_CITIES_URL_SLUGS_BY_LOWER


def parse_geo_offer_search_settings_from_string(s: str) -> Union[GeoOfferSearchSettings, ErrorMessageToUser]:
    try:
        raw_user_city, raw_user_radius_search = s.split(",")
    except ValueError:
        return ErrorMessageToUser(message=(
            "Сообщение не соответсвует формату ❌\nНазвание города и радиус поиска в километрах должны быть через запятую"
        ))

    user_city, user_radius_search = raw_user_city.strip().lower(), raw_user_radius_search.strip()

    find_city = RU_CITIES_URL_SLUGS_BY_LOWER.get(user_city)
    if find_city:
        return GeoOfferSearchSettings(
            city=find_city.city,
            city_url_slug=find_city.city_url_slug,
            radius_search=user_radius_search
        )

    return ErrorMessageToUser(message=(
        f"Город «{raw_user_city}» не найден ❌"
        "\nПроверьте правильность названия города или обратитесь к автору бота выяснения проблемы"
    ))
