from datetime import datetime, timedelta, timezone
import os
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_jwt_extended.utils import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
)

from jwt.exceptions import InvalidSignatureError

from app import app, db, jwt
from models import Role, TokenBlocklist, User
from routes import resources


@app.before_first_request
def initialize_db():
    db.create_all()
    for name in ["customer", "seller", "admin"]:
        db.session.add(Role(name=name, description=name))
    db.session.commit()


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


@app.errorhandler(InvalidSignatureError)
@app.errorhandler(NoAuthorizationError)
def jwt_exception_handler(exception):
    app.logger.exception(exception)
    return "Unauthorized", 401


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone(timedelta(hours=+8)))
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


app.register_blueprint(resources)

port = int(os.environ.get("PORT", 8080))
if __name__ == "__main__":
    app.run(threaded=True, host="127.0.0.1", port=port)
