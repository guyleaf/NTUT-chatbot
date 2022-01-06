from datetime import datetime, timedelta, timezone
import os

from flask import request
from flask_jwt_extended.utils import (
    create_access_token,
    get_jwt,
    current_user,
    set_access_cookies,
)

from werkzeug.utils import redirect

from app import app, db, jwt
from exceptions import UnauthorizedAccessException
from models import Role, TokenBlocklist, User
from routes import resources
from helpers import save_redirect_data, make_api_response


@app.before_first_request
def initialize_db():
    # if app.config["ENV"] == "development":
    #     db.drop_all()

    db.create_all()
    # for name in ["customer", "seller", "admin"]:
    #     role = Role.query.filter_by(name=name).one_or_none()
    #     if role is None:
    #         db.session.add(Role(name=name, description=name))
    # db.session.commit()


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(_, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).scalar()
    return token is not None


def redirect_to_login():
    save_redirect_data(request.url_rule.endpoint)
    print(request)
    if request.content_type and "application/json" in request.content_type:
        return make_api_response(
            False, "Please Login First", {"redirect": "/login"}
        )
    return redirect("/login")


@app.errorhandler(UnauthorizedAccessException)
def handle_unauthorized_access(e: UnauthorizedAccessException):
    message = e.message
    if request.content_type and "application/json" in request.content_type:
        return make_api_response(False, message), 401
    else:
        return message, 401


@jwt.unauthorized_loader
def jwt_exception_handler(_):
    save_redirect_data(request.url_rule.endpoint)
    return redirect_to_login()


@jwt.invalid_token_loader
@jwt.revoked_token_loader
@jwt.user_lookup_error_loader
@jwt.expired_token_loader
def token_handler(_jwt_header, _jwt_payload):
    save_redirect_data(request.url_rule.endpoint)
    return redirect_to_login()


@app.after_request
def refresh_expiring_jwts(response):
    try:
        token = get_jwt()
        exp_timestamp = token["exp"]
        now = datetime.now(timezone(timedelta(hours=+8)))
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=current_user)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


app.register_blueprint(resources)

port = int(os.environ.get("PORT", 8080))
if __name__ == "__main__":
    app.run(threaded=True, host="127.0.0.1", port=port)
