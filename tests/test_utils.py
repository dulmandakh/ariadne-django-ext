from ariadne_django_ext import utils
from django.core.exceptions import PermissionDenied

import pytest


def test_is_authenticated(user_request):
    user = getattr(user_request, "user", None)
    is_active = user and user.is_active
    if is_active:
        assert user == utils.is_authenticated(user_request)
    else:
        with pytest.raises(PermissionDenied):
            utils.is_authenticated(user_request)

        # check is_active, don't raise
        assert utils.is_authenticated(user_request, True, False) == None
        if user:
            assert utils.is_authenticated(user_request, False) == user
