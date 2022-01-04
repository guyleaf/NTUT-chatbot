﻿import secrets
from datetime import datetime, timedelta, timezone
from flask import (
    Blueprint,
    url_for,
    request,
    abort,
    redirect,
)
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    current_user,
)
from flask_jwt_extended.utils import get_jwt

from app import oauth_client, db
from models import Role, TokenBlocklist, User
from helpers import get_redirect_data

auth_resource = Blueprint("auth", __name__, static_folder="templates")


@auth_resource.route("/login", methods=["GET"])
def login():
    redirect_uri = url_for("auth", _external=True)
    return oauth_client.authorize_redirect(redirect_uri)


@auth_resource.route("/auth", methods=["GET"])
def auth():
    code = request.args.get("code")
    state = request.args.get("state")
    if code is None or state is None:
        abort(400)

    user = oauth_client.authorize_access_token()
    if user is None:
        abort(500)

    user_data = User.query.filter_by(line_id=user["lineId"]).one_or_none()

    if user_data is None:
        customer_role = Role.query.filter_by(name="customer").one_or_none()
        user_data = User(
            id=secrets.token_hex(16),
            username=user["username"],
            line_id=user["lineId"],
            email=user["email"],
            role=customer_role,
        )
        db.session.add(user_data)
        db.session.commit()

    access_token = create_access_token(identity=user_data)
    response = redirect(url_for("redirect_route", **get_redirect_data()))
    set_access_cookies(response, access_token)
    return response


@auth_resource.route("/logout")
@jwt_required
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone(timedelta(hours=+8)))
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()

    response = redirect("/")
    unset_jwt_cookies(response)
    return response


@auth_resource.route("/me", methods=["GET"])
@jwt_required()
def protected():
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.name,
    }
