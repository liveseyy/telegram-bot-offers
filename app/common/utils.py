from typing import Iterable
from asgiref.sync import sync_to_async


def convert_sync_queryset_to_async(queryset):
    return sync_to_async(list)(queryset)


def convert_sync_func_to_async(func):
    return sync_to_async(func)


def method_cache_key(cache_prefix="cache", method="unknown", **kwargs) -> str:
    # не использовать inspect.stack()[1][3] – это очень медленно!
    sign_string = [cache_prefix, method]
    for k, v in dict(kwargs).items():
        sign_string.append("%s__%s" % (k, v))
    return "@".join(sign_string)


def iterable_has_only_digits(iterable: Iterable):
    return all(
        [
            isinstance(watcher_id, int) or (isinstance(watcher_id, str) and watcher_id.isdigit())
            for watcher_id in iterable
        ]
    )
