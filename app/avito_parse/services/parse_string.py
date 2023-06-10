from typing import NamedTuple, Optional

from avito_parse.geo_offer_search_settings import GeoOfferSearchSettings, RU_CITIES_URL_SLUGS_BY_LOWER


def parse_geo_offer_search_settings_from_string(s: str) -> Optional[GeoOfferSearchSettings]:
    raw_user_city, raw_user_radius_search = s.split(",")
    user_city, user_radius_search = raw_user_city.strip().lower(), raw_user_radius_search.strip()

    find_city = RU_CITIES_URL_SLUGS_BY_LOWER.get(user_city)
    if find_city:
        return GeoOfferSearchSettings(
            city=find_city.city,
            city_url_slug=find_city.city_url_slug,
            radius_search=user_radius_search
        )
