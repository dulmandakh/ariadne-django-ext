from base64 import b64encode

import pytest
from django.core.exceptions import PermissionDenied

from ariadne_django_ext import decorators

from .conftest import password


def test_allow_basic_auth(user, rf, django_user_model):
    return_value = "return_value"

    @decorators.allow_basic_auth
    @decorators.login_required
    def view(_):
        return return_value

    request = rf.get("/")
    if user:
        request.META["HTTP_AUTHORIZATION"] = "Basic {}".format(
            b64encode(f"{user.username}:{password}".encode()).decode()
        )

    assert getattr(request, "user", None) is None
    if user and user.is_active:
        assert view(request) == return_value
    else:
        with pytest.raises(PermissionDenied):
            view(request)


def test_login_required(user_request):
    return_value = "return_value"

    @decorators.login_required
    def view(_):
        return return_value

    user = getattr(user_request, "user", None)
    if user and user.is_active:
        assert view(user_request) == return_value
    else:
        with pytest.raises(PermissionDenied):
            view(user_request)


def test_wrap_result():
    @decorators.wrap_result(key="key")
    def resolver():
        return "result"

    assert resolver() == {"key": "result"}
