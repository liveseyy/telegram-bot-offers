from django.utils import timezone
from avito_parse.filter_forms.exceptions import BadUserInputOption


NONE_INPUT_USER_CHAR = "-"


def base_validator(func):
    def wrapper(user_input: str):
        user_input = user_input.strip()

        if user_input == NONE_INPUT_USER_CHAR:
            return None

        return func(user_input)
    return wrapper


@base_validator
def positive_integer(user_input: str):
    try:
        user_input = int(user_input)
    except ValueError:
        raise BadUserInputOption(option_verbose_name="todo")

    if user_input < 0:
        raise BadUserInputOption(option_verbose_name="todo")

    return user_input


@base_validator
def year(user_input: str):
    user_input_year = positive_integer(user_input)

    if user_input_year > timezone.localtime().year:
        raise BadUserInputOption(option_verbose_name="todo")

    return user_input_year


@base_validator
def alpha_numeric_with_spaces(user_input: str):
    if not user_input.replace(" ", "").replace("(", "").replace(")", "").replace(".", "")\
            .replace("-", "").isalnum():
        raise BadUserInputOption(option_verbose_name="todo")

    return user_input
