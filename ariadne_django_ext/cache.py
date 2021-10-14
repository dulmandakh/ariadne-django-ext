from functools import partial, wraps
from typing import Callable, Union

from django.core.cache import cache as dj_cache

default = "ariadne-django-ext"
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


def cache(key: Union[str, Callable], **cache_kwargs):
    def wrap_resolver(resolver: Callable):
        @wraps(resolver)
        def wrapper(parent, info, **kwargs):
            resolve = partial(resolver, parent, info, **kwargs)
            cache_key = key(parent, info, **kwargs) if callable(key) else key
            if cache_key is not None:
                cache_key = cache_keygen(info, cache_key)
                cached = dj_cache.get(cache_key, default, **cache_kwargs)
                if cached != default:
                    return cached

                result = resolve()
                dj_cache.add(cache_key, result, **cache_kwargs)
                return result
            return resolve()

        return wrapper

    return wrap_resolver
