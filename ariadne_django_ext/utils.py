from django.core.exceptions import PermissionDenied


def is_authenticated(request, is_active=False, raise_exception=False):
    user = getattr(request, "user")
    if user and user.is_authenticated and (not is_active or user.is_active):
        return user
    if raise_exception:
        raise PermissionDenied()
