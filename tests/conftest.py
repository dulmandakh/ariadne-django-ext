import pytest


@pytest.fixture(
    ids=["anonymous", "not-active", "authenticated"],
    params=[None, False, True],
)
def user(request, django_user_model):
    if request.param is not None:
        return django_user_model.objects.create(
            username="someone", password="something", is_active=request.param
        )


@pytest.fixture
def user_request(user, rf):
    request = rf.get("/customer/details")
    request.user = user
    return request
