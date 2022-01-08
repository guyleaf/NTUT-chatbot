import json
from functools import wraps
from flask import session, request
from flask_jwt_extended import current_user
from flask_jwt_extended import verify_jwt_in_request

from exceptions import UnauthorizedAccessException


def jwt_required(
    optional=False,
    fresh=False,
    refresh=False,
    locations=None,
    remember_endpoint: bool = False,
):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request(optional, fresh, refresh, locations)
            finally:
                if remember_endpoint:
                    save_watched_endpoint()

            return fn(*args, **kwargs)

        return decorator

    return wrapper


def roles_accepted(roles: "list[str]", remember_endpoint: bool = False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
            finally:
                if remember_endpoint:
                    save_watched_endpoint()

            role_name = current_user.user.role.name
            if role_name in roles:
                return fn(*args, **kwargs)
            else:
                raise UnauthorizedAccessException()

        return decorator

    return wrapper


def save_watched_endpoint():
    args = request.args.to_dict()
    args.update(request.view_args)
    session["last_watched_endpoint"] = {
        "page": request.endpoint,
        "args": json.dumps(args),
    }
