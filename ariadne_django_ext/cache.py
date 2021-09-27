from functools import wraps
from typing import Callable, Union

from django.core.cache import cache as dj_cache


def cache(key: Union[str, Callable], **djkwargs):
    def wrap_resolver(resolver: Callable):
        @wraps(resolver)
        def wrapper(parent, info, **kwargs):
            cache_key = key(parent, info) if callable(key) else key
            cached = dj_cache.get(cache_key)
            if cached is not None:
                return cached

            result = resolver(parent, info, **kwargs)
            if result is not None:
                dj_cache.add(cache_key, result, **djkwargs)
            return result

        return wrapper

    return wrap_resolver
