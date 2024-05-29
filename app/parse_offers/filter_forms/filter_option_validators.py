from django.utils import timezone
from parse_offers.filter_forms.exceptions import BadUserInputOption


NONE_INPUT_USER_CHAR = "-"


def base_validator(func):
    def wrapper(user_input: str, *args, **kwargs):
        user_input = user_input.strip()

        if user_input == NONE_INPUT_USER_CHAR or user_input == "":
            return None

        return func(user_input, *args, **kwargs)
    return wrapper


@base_validator
def positive_integer_with_spaces(user_input: str, with_spaces: bool = True):
    """
    90000
    90 000 000
    """
    try:
        if with_spaces:
            user_input = user_input.replace(" ", "")
        user_input = int(user_input)
    except ValueError:
        raise BadUserInputOption(option_verbose_name="todo")

    if user_input < 0:
        raise BadUserInputOption(option_verbose_name="todo")

    return user_input


@base_validator
def year(user_input: str):
    user_input_year = positive_integer_with_spaces(user_input=user_input, with_spaces=False)

    if user_input_year > timezone.localtime().year:
        raise BadUserInputOption(option_verbose_name="todo")

    return user_input_year


@base_validator
def alpha_numeric_with_spaces(user_input: str):
    if not user_input.replace(" ", "").replace("(", "").replace(")", "").replace(".", "")\
            .replace("-", "").isalnum():
        raise BadUserInputOption(option_verbose_name="todo")

    return user_input
