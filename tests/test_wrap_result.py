from ariadne_django_ext import wrap_result


def test_wrap_result():
    @wrap_result(key="key")
    def resolver():
        return "result"

    assert resolver() == {"key": "result"}
