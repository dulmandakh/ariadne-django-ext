from base64 import b64decode
from functools import wraps

from django.contrib.auth import authenticate

from .utils import is_authenticated


def allow_basic_auth(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_authenticated(request):
            http_auth = request.META.get("HTTP_AUTHORIZATION")
            if http_auth and http_auth.startswith("Basic"):
                try:
                    _, token = http_auth.split()
                    username, password = b64decode(token).decode().split(":")
                    user = authenticate(
                        request=request, username=username, password=password
                    )
                    if user and user.is_active:
                        request.user = user
                except Exception:
                    pass
        return view_func(request, *args, **kwargs)

    return wrapper


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if is_authenticated(request, is_active=True, raise_exception=True):
            return view_func(request, *args, **kwargs)

    return wrapper


def wrap_result(key: str):
    def wrap_resolver(resolver):
        @wraps(resolver)
        def wrapper(*args, **kwargs):
            return {key: resolver(*args, **kwargs)}

        return wrapper

    return wrap_resolver
