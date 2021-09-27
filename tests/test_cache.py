from unittest.mock import Mock

from django.core.cache import cache as dj_cache
from django.db import models

from ariadne_django_ext import cache


class MyModel(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        app_label = "tests"


def test_cache_key_callable():
    return_value = "result"
    resolver = Mock(return_value=return_value)
    cached_resolver = cache(key=lambda parent, _: parent)(resolver)

    for i in range(5):
        assert cached_resolver(i, None) == return_value
        assert cached_resolver(i, False) == return_value
        assert cached_resolver(i, True) == return_value
        assert dj_cache.get(i) == return_value

        resolver.assert_called_once()
        resolver.assert_called_with(i, None)
        resolver.reset_mock()


def test_cache_key_str():
    key = "key_str"
    return_value = "result"

    resolver = Mock(return_value=return_value)
    cached_resolver = cache(key=key)(resolver)

    assert cached_resolver(None, None) == return_value
    assert cached_resolver(None, None) == cached_resolver(True, False)
    assert cached_resolver(True, False) == cached_resolver(False, True)
    assert dj_cache.get(key) == return_value

    resolver.assert_called_once()


def test_cache_result_none():
    # None value won't be cached
    key = "result_none"

    resolver = Mock(return_value=None)
    cached_resolver = cache(key=key)(resolver)

    assert cached_resolver(None, None) is None
    assert cached_resolver(None, None) is None
    assert dj_cache.get(key, True) is True

    resolver.assert_called()
