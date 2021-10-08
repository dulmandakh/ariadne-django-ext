from functools import wraps


def wrap_result(key: str):
    def wrap_resolver(resolver):
        @wraps(resolver)
        def wrapper(*args, **kwargs):
            return {key: resolver(*args, **kwargs)}

        return wrapper

    return wrap_resolver
