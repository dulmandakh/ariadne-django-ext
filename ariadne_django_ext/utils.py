from django.core.exceptions import PermissionDenied


def is_authenticated(request):
    user = getattr(request, "user")
    if user and user.is_authenticated and user.is_active:
        return user
    raise PermissionDenied()
