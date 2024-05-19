import logging
from dataclasses import dataclass, field
from abc import ABC
from typing import Callable, NamedTuple, List

from parse_offers.filter_forms.filter_option_validators import (
    NONE_INPUT_USER_CHAR,
    positive_integer_with_spaces,
    alpha_numeric_with_spaces,
    year
)
from parse_offers.filter_forms.exceptions import BadUserInputOption
from parse_offers.offer_structure import ParsedOffer

logger = logging.getLogger("sync_watchers_with_offers")


class FilterOption(NamedTuple):
    key: str
    verbose_name: str
    validator: Callable


@dataclass
class FilterFormResult:
    specific_filter: dict = field(default_factory=dict)

    validation_recognized_fields_errors: List[str] = field(default_factory=list)
    validation_not_recognized_fields_errors: List[str] = field(default_factory=list)


class BaseFilterForm(ABC):
    """
    Форма заполнения фильтров для поиска объявлений.

    Занимается валидацией заполненной формы, форматировананием сообщений,
        валидацией объявлений по заданным фильтрам пользователя.
    """
    MESSAGE: str = ...

    PRICE_FROM_OPTION = FilterOption(
        key="price_from",
        verbose_name="Цена, от",
        validator=positive_integer_with_spaces,
    )
    PRICE_TO_OPTION = FilterOption(
        key="price_to",
        verbose_name="Цена, до",
        validator=positive_integer_with_spaces,
    )


class FilterFormTransport(BaseFilterForm):
    BRAND_MODEL_OPTION = FilterOption(
        key="brand_model",
        verbose_name="Марка, модель",
        validator=alpha_numeric_with_spaces,
    )
    YEAR_FROM_OPTION = FilterOption(
        key="year_from",
        verbose_name="Год, от",
        validator=year,
    )
    YEAR_TO_OPTION = FilterOption(
        key="year_to",
        verbose_name="Год, до",
        validator=year,
    )
    MILEAGE_FROM_OPTION = FilterOption(
        key="mileage_from",
        verbose_name="Пробег, от",
        validator=positive_integer_with_spaces,
    )
    MILEAGE_TO_OPTION = FilterOption(
        key="mileage_to",
        verbose_name="Пробег, до",
        validator=positive_integer_with_spaces,
    )

    VERBOSE_NAME_TO_OPTION_MAP = {
        BRAND_MODEL_OPTION.verbose_name: BRAND_MODEL_OPTION,
        YEAR_FROM_OPTION.verbose_name: YEAR_FROM_OPTION,
        YEAR_TO_OPTION.verbose_name: YEAR_TO_OPTION,
        MILEAGE_FROM_OPTION.verbose_name: MILEAGE_FROM_OPTION,
        MILEAGE_TO_OPTION.verbose_name: MILEAGE_TO_OPTION,
        BaseFilterForm.PRICE_FROM_OPTION.verbose_name: BaseFilterForm.PRICE_FROM_OPTION,
        BaseFilterForm.PRICE_TO_OPTION.verbose_name: BaseFilterForm.PRICE_TO_OPTION,
    }

    MESSAGE = f"Отправьте мне заполненную форму, скопировав шаблон." \
              f" В невлияющих параметрах оставьте прочерк." \
              f" Не важно заглавные или прописные буквы.\n\n" \
              f"Нажмите чтобы скопировать:\n" \
              f"<code>{BRAND_MODEL_OPTION.verbose_name}: {NONE_INPUT_USER_CHAR}\n" \
              f"{YEAR_FROM_OPTION.verbose_name}: {NONE_INPUT_USER_CHAR}\n" \
              f"{YEAR_TO_OPTION.verbose_name}: {NONE_INPUT_USER_CHAR}\n" \
              f"{MILEAGE_FROM_OPTION.verbose_name}: {NONE_INPUT_USER_CHAR}\n" \
              f"{MILEAGE_TO_OPTION.verbose_name}: {NONE_INPUT_USER_CHAR}\n" \
              f"{BaseFilterForm.PRICE_FROM_OPTION.verbose_name}: {NONE_INPUT_USER_CHAR}\n" \
              f"{BaseFilterForm.PRICE_TO_OPTION.verbose_name}: {NONE_INPUT_USER_CHAR}</code>\n\n" \
              f"Пример заполненной формы:\n\n" \
              f"{BRAND_MODEL_OPTION.verbose_name}: Kia Ceed\n" \
              f"{YEAR_FROM_OPTION.verbose_name}: 2016\n" \
              f"{YEAR_TO_OPTION.verbose_name}: 2019\n" \
              f"{MILEAGE_FROM_OPTION.verbose_name}: -\n" \
              f"{MILEAGE_TO_OPTION.verbose_name}: 90 000\n" \
              f"{BaseFilterForm.PRICE_FROM_OPTION.verbose_name}: -\n" \
              f"{BaseFilterForm.PRICE_TO_OPTION.verbose_name}: 1 200 000\n\n" \
              f"Отправку формы можно отменить нажав кнопку (отменится автоматически через 1 час):" \

    @classmethod
    def get_formatted_message(cls, user_id: int):
        return cls.MESSAGE.format(userId=user_id)

    @classmethod
    def process_user_filter_form(cls, text: str) -> FilterFormResult:
        filter_result = cls._parse_user_options(text=text)
        return filter_result

    @classmethod
    def process_user_filter_web_form(cls, data: dict) -> FilterFormResult:
        filter_result = cls._get_filter_form_result_from_dict(data=data)
        return filter_result

    @classmethod
    def _get_filter_form_result_from_dict(cls, data: dict) -> FilterFormResult:
        result = FilterFormResult()
        for option in cls.VERBOSE_NAME_TO_OPTION_MAP.values():
            result.specific_filter[option.key] = data[option.key]

        return result


    @classmethod
    def _parse_user_options(cls, text: str) -> FilterFormResult:
        options_rows = text.split("\n")
        result = FilterFormResult()
        for user_option in options_rows:
            try:
                verbose_name, user_input = user_option.split(":")
            except ValueError:
                result.validation_not_recognized_fields_errors.append(user_option)
                continue

            verbose_name = verbose_name.strip().capitalize()

            filter_option = cls.VERBOSE_NAME_TO_OPTION_MAP.get(verbose_name)
            if filter_option is None:
                result.validation_not_recognized_fields_errors.append(user_option)
                continue

            try:
                user_input = filter_option.validator(user_input)
                result.specific_filter[filter_option.key] = user_input
            except BadUserInputOption:
                result.validation_recognized_fields_errors.append(filter_option.verbose_name)

        return result

    @classmethod
    def parsed_offer_is_match_filter(cls,
                                     parsed_offer: ParsedOffer,
                                     specific_filter: dict) -> bool:
        logger.debug(f"Compare: {parsed_offer=}, {specific_filter=}")

        parsed_brand_model = parsed_offer.model_brand
        parsed_year = parsed_offer.year

        watcher_brand_model = specific_filter[cls.BRAND_MODEL_OPTION.key]
        logger.debug(f"Compare watcher_brand_model: {watcher_brand_model=}, {parsed_brand_model=}")
        if watcher_brand_model is not None and watcher_brand_model.lower() != parsed_brand_model.lower():
            logger.debug(f"Miss watcher_brand_model: {watcher_brand_model=}, {parsed_brand_model=}")
            return False

        watcher_year_from = specific_filter[cls.YEAR_FROM_OPTION.key]
        logger.debug(f"Compare watcher_brand_model: {watcher_brand_model=}, {parsed_brand_model=}")
        if watcher_year_from is not None and watcher_year_from > parsed_year:
            logger.debug(f"Miss watcher_year_from: {watcher_year_from=}, {parsed_year=}")
            return False

        watcher_year_to = specific_filter[cls.YEAR_TO_OPTION.key]
        if watcher_year_to is not None and watcher_year_to < parsed_year:
            logger.debug(f"Miss watcher_year_to: {watcher_year_to=}, {parsed_year=}")
            return False

        parsed_price = int(parsed_offer.price)
        watcher_price_from = specific_filter[cls.PRICE_FROM_OPTION.key]
        if watcher_price_from is not None and not (watcher_price_from >= parsed_price):
            logger.debug(f"Miss watcher_price_from: {watcher_price_from=}, {parsed_price=}")
            return False

        watcher_price_to = specific_filter[cls.PRICE_TO_OPTION.key]
        if watcher_price_to is not None and not (watcher_price_to <= parsed_price):
            logger.debug(f"Miss watcher_price_to: {watcher_price_to=}, {parsed_price=}")
            return False

        if parsed_offer.mileage:
            parsed_mileage = int(parsed_offer.mileage.replace("км", " ").replace(" ", "").strip())
            watcher_mileage_from = specific_filter[cls.MILEAGE_FROM_OPTION.key]
            if watcher_mileage_from is not None and not (watcher_mileage_from >= parsed_mileage):
                logger.debug(f"Miss watcher_mileage_from: {watcher_mileage_from=}, {parsed_mileage=}")
                return False

            watcher_mileage_to = specific_filter[cls.MILEAGE_TO_OPTION.key]
            if watcher_mileage_to is not None and not (watcher_mileage_to <= parsed_mileage):
                logger.debug(f"Miss watcher_mileage_to: {watcher_mileage_to=}, {parsed_mileage=}")
                return False

        logger.debug(f"Found match offer: {parsed_offer=}, {specific_filter=}")

        return True

    @classmethod
    def format_specific_filter_to_verbose_name(cls, specific_filter: dict) -> str:
        # замена None на пустое значение для форматирования
        for key, value in specific_filter.items():
            if value is None:
                specific_filter[key] = NONE_INPUT_USER_CHAR

        result_message = (
            f"{cls.BRAND_MODEL_OPTION.verbose_name}: {{{cls.BRAND_MODEL_OPTION.key}}}\n"
            f"{cls.YEAR_FROM_OPTION.verbose_name}: {{{cls.YEAR_FROM_OPTION.key}}}\n"
            f"{cls.YEAR_TO_OPTION.verbose_name}: {{{cls.YEAR_TO_OPTION.key}}}\n"
            f"{cls.MILEAGE_FROM_OPTION.verbose_name}: {{{cls.MILEAGE_FROM_OPTION.key}}}\n"
            f"{cls.MILEAGE_TO_OPTION.verbose_name}: {{{cls.MILEAGE_TO_OPTION.key}}}\n"
            f"{cls.PRICE_FROM_OPTION.verbose_name}: {{{cls.PRICE_FROM_OPTION.key}}}\n"
            f"{cls.PRICE_TO_OPTION.verbose_name}: {{{cls.PRICE_TO_OPTION.key}}}"
        )
        return result_message.format(**specific_filter)
