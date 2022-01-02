import os
from datetime import datetime, timezone, timedelta

from flask import url_for, session, request, abort, render_template, redirect
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    set_access_cookies,
    get_jwt_identity,
    get_jwt,
    unset_jwt_cookies,
)
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import InvalidSignatureError

from helpers import save_redirect_data, get_redirect_data
from app import app, db, oauth_client
from models import User


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


@app.errorhandler(InvalidSignatureError)
@app.errorhandler(NoAuthorizationError)
def jwt_exception_handler(exception):
    app.logger.exception(exception)
    return "Unauthorized", 401


@app.route("/")
def home():
    user = session.get("user")
    return render_template("home.html", user=user)


@app.route("/redirect")
def redirect_route():
    page = request.args.get("page", "home")
    return redirect(url_for(page))


@app.route("/test")
def test():
    user = session.get("user")
    if user is None:
        save_redirect_data(request.endpoint)
        return redirect(url_for("login"))

    return user


@app.route("/login", methods=["GET"])
def login():
    redirect_uri = url_for("auth", _external=True)
    return oauth_client.authorize_redirect(redirect_uri)


@app.route("/auth", methods=["GET"])
def auth():
    code = request.args.get("code")
    state = request.args.get("state")
    if code is None or state is None:
        abort(400)

    user = oauth_client.authorize_access_token()
    if user is None:
        abort(500)

    user_data = User.query.filter_by(line_id=user["lineId"]).first()

    if user_data is None:
        access_token = create_access_token(
            identity=user["lineId"], fresh=True, additional_claims=user
        )
        response = redirect(url_for("email_registration_page"))
    else:
        additional_claims = {
            "username": user_data.username,
            "lineId": user_data.line_id,
            "role": user_data.role.name,
        }
        access_token = create_access_token(
            identity=user_data.id, additional_claims=additional_claims
        )
        response = redirect(url_for("redirect_route", **get_redirect_data()))

    set_access_cookies(response, access_token)
    return response


@app.route("/email", methods=["GET"])
@jwt_required(fresh=True)
def email_registration_page():
    return "email_page"


@app.route("/email", methods=["POST"])
@jwt_required
def register_email():
    pass


@app.route("/logout")
def logout():
    response = redirect("/")
    unset_jwt_cookies(response)
    return response


port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
    app.run(threaded=True, host="127.0.0.1", port=port)
