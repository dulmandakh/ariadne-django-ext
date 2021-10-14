from functools import partial, wraps
from typing import Callable, Union

from django.core.cache import cache as dj_cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

default = object()
delimiter = "::"


def cache_keygen(info, key):
    return "{}{delimiter}{}{delimiter}{}".format(
        info.path.typename,
        info.path.key,
        delimiter.join(str(k) for k in key)
        if isinstance(key, tuple) or isinstance(key, list)
        else key,
        delimiter=delimiter,
    )


def cache(key: Union[str, Callable], timeout=DEFAULT_TIMEOUT, version=None):
    def wrap_resolver(resolver: Callable):
        @wraps(resolver)
        def wrapper(parent, info, **kwargs):
            resolve = partial(resolver, parent, info, **kwargs)
            cache_key = key(parent, info, **kwargs) if callable(key) else key
            if cache_key is not None:
                cache_key = cache_keygen(info, cache_key)
                cached = dj_cache.get(cache_key, default, version)
                if cached != default:
                    return cached

                result = resolve()
                dj_cache.add(cache_key, result, timeout, version)
                return result
            return resolve()

        return wrapper

    return wrap_resolver
