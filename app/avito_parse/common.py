from datetime import datetime, timedelta
from django.utils import timezone


def parse_datetime(str_datetime: str) -> datetime:
    """
    14 мая 11:24 -> datetime(year=текущий_год, month=5, day=14, hour=11, minute=24)
    """
    verbose_month_map = {
        "января": 1,
        "февраля": 2,
        "марта": 3,
        "апреля": 4,
        "мая": 5,
        "июня": 6,
        "июля": 7,
        "августа": 8,
        "сентября": 9,
        "октября": 10,
        "ноября": 11,
        "декабря": 12,
    }
    day, verbose_month, raw_datetime = str_datetime.split(" ")
    hours, minutes = raw_datetime.split(":")
    year_now = datetime.today().year
    return datetime(
        year=year_now,
        month=verbose_month_map[verbose_month],
        day=int(day),
        hour=int(hours),
        minute=int(minutes),
        tzinfo=timezone.tzinfo()
    )


def parse_show_up_time_ago(show_up_time_ago: str, time_from: datetime) -> datetime:
    dates_words = show_up_time_ago.split(" ")
    result = None
    if "сек" in dates_words[1]:
        result = time_from

    if "мин" in dates_words[1]:
        result = time_from - timedelta(minutes=int(dates_words[0]) + 1)

    elif "час" in dates_words[1]:
        result = time_from - timedelta(hours=int(dates_words[0]))

    return result
