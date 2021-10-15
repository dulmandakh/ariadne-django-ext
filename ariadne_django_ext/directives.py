from ariadne import SchemaDirectiveVisitor
from django.core.exceptions import PermissionDenied
from graphql import default_field_resolver

from .utils import is_authenticated


class IsAuthenticatedDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, _):
        original_resolver = field.resolve or default_field_resolver

        def resolve_for_authenticated_user(parent, info, **kwargs):
            user = is_authenticated(
                info.context["request"], is_active=True, raise_exception=True
            )
            return original_resolver(parent, info, user=user, **kwargs)

        field.resolve = resolve_for_authenticated_user
        return field


class IsStaffDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, _):
        original_resolver = field.resolve or default_field_resolver

        def resolve_for_authenticated_user(parent, info, **kwargs):
            user = is_authenticated(info.context["request"], is_active=True)
            if user and user.is_staff:
                return original_resolver(parent, info, user=user, **kwargs)
            raise PermissionDenied()

        field.resolve = resolve_for_authenticated_user
        return field
