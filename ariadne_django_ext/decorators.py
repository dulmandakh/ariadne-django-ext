from functools import wraps

from .utils import is_authenticated


def login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if is_authenticated(request):
            return view(request, *args, **kwargs)

    return wrapper


def wrap_result(key: str):
    def wrap_resolver(resolver):
        @wraps(resolver)
        def wrapper(*args, **kwargs):
            return {key: resolver(*args, **kwargs)}

        return wrapper

    return wrap_resolver
