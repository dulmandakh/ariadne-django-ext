import pytest
from django.core.exceptions import PermissionDenied

from ariadne_django_ext.decorators import login_required


def test_login_required(user_request):
    return_value = "return_value"

    @login_required
    def view(request):
        return return_value

    user = getattr(user_request, "user", None)
    if user and user.is_active:
        assert view(user_request) == return_value
    else:
        with pytest.raises(PermissionDenied):
            view(user_request)
