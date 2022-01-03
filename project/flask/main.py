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

from app import app, db
from routes import resources


# Create a user to test with
@app.before_first_request
def initialize_db():
    db.create_all()


@app.errorhandler(InvalidSignatureError)
@app.errorhandler(NoAuthorizationError)
def jwt_exception_handler(exception):
    app.logger.exception(exception)
    return "Unauthorized", 401


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
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
