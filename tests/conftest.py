import pytest

password = "something"


@pytest.fixture(
    ids=["anonymous", "not-active", "authenticated"],
    params=[None, False, True],
)
def user(request, django_user_model):
    if request.param is not None:
        user = django_user_model.objects.create(
            username="someone", is_active=request.param
        )
        user.set_password(password)
        user.save(update_fields=["password"])
        return user


@pytest.fixture
def user_request(user, rf):
    request = rf.get("/customer/details")
    request.user = user
    return request
