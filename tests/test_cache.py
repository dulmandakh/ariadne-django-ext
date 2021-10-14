from unittest.mock import Mock

from django.core.cache import cache as dj_cache

from ariadne_django_ext.cache import cache, cache_keygen, delimiter


class GraphQLInfo:
    def __init__(self, typename, key):
        self.path = GraphQLInfoPath(typename, key)


class GraphQLInfoPath:
    def __init__(self, typename, key):
        self.key = key
        self.typename = typename


def test_cache_keygen():
    typename, key = "typename", "key"
    prefix = "{}{delimiter}{}".format(typename, key, delimiter=delimiter)
    info = GraphQLInfo(typename, key)

    assert cache_keygen(info, 1) == "{}{delimiter}{}".format(
        prefix, str(1), delimiter=delimiter
    )
    assert cache_keygen(info, "1") == "{}{delimiter}{}".format(
        prefix, "1", delimiter=delimiter
    )
    assert cache_keygen(info, True) == "{}{delimiter}{}".format(
        prefix, str(True), delimiter=delimiter
    )
    assert cache_keygen(info, (1, 2)) == "{}{delimiter}{}{delimiter}{}".format(
        prefix, str(1), str(2), delimiter=delimiter
    )
    assert cache_keygen(info, [1, 2]) == "{}{delimiter}{}{delimiter}{}".format(
        prefix, str(1), str(2), delimiter=delimiter
    )


def test_cache_key_callable():
    dj_cache.clear()
    return_value = "result"

    info = GraphQLInfo("typename", "key")
    for key_callable in (
        lambda parent, _: parent,
        lambda *_: "key",
        lambda *_: True,
        lambda *_: (1, 2, 3),
        lambda *_: [1, 2, 4],
    ):
        resolver = Mock(return_value=return_value)
        cached_resolver = cache(key=key_callable)(resolver)
        assert cached_resolver(0, info) == return_value
        assert cached_resolver(0, info) == return_value
        resolver.assert_called_once()


def test_cache_key_none():
    dj_cache.clear()
    return_value = "result"

    info = GraphQLInfo("typename", "key")
    resolver = Mock(return_value=return_value)
    for cache_key in (None, lambda *_: None):
        cached_resolver = cache(key=cache_key)(resolver)
        for parent in (None, False, True):
            assert cached_resolver(parent, info) == return_value
            resolver.assert_called_with(parent, info)


def test_cache_key_value():
    dj_cache.clear()
    info = GraphQLInfo("typename", "key")
    return_value = "result"

    for cache_key in ("key", 1, True, False, (1, 2, 3), [1, 2, 4]):
        resolver = Mock(return_value=return_value)
        cached_resolver = cache(key=cache_key)(resolver)
        assert cached_resolver(0, info) == return_value
        assert cached_resolver(1, info) == return_value

        resolver.assert_called_once()
        resolver.assert_called_with(0, info)
