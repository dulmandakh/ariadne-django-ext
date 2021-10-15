from ariadne import SchemaDirectiveVisitor
from graphql import default_field_resolver

from .utils import PermissionDenied, is_authenticated


class IsAuthenticatedDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, _):
        original_resolver = field.resolve or default_field_resolver

        def resolve_for_authenticated_user(parent, info, **kwargs):
            user = is_authenticated(info.context["request"])
            if user:
                return original_resolver(parent, info, user=user, **kwargs)

        field.resolve = resolve_for_authenticated_user
        return field


class IsStaffDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, _):
        original_resolver = field.resolve or default_field_resolver

        def resolve_for_authenticated_user(parent, info, **kwargs):
            user = is_authenticated(info.context["request"])
            if user and user.is_staff:
                return original_resolver(parent, info, user=user, **kwargs)
            raise PermissionDenied()

        field.resolve = resolve_for_authenticated_user
        return field
