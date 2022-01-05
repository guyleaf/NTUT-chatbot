from functools import wraps
from flask_jwt_extended import current_user
from flask_jwt_extended import verify_jwt_in_request

from exceptions import UnauthorizedAccessException


def roles_accepted(roles: list[str]):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            role_name = current_user.role.name
            if role_name in roles:
                return fn(*args, **kwargs)
            else:
                raise UnauthorizedAccessException()

        return decorator

    return wrapper
