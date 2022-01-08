import secrets
from datetime import datetime, timedelta, timezone
from flask import Blueprint, url_for, request, abort, redirect, session
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    current_user,
)
from flask_jwt_extended.utils import get_jwt

from app import oauth_client, db, firestoreDAO
from decorators import jwt_required
from models import Role, TokenBlocklist, User

auth_resource = Blueprint("auth", __name__, static_folder="templates")


@auth_resource.route("/login", methods=["GET"])
def login():
    redirect_uri = url_for("resources.auth.auth", _external=True)
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
        firestoreDAO.initialize_data_for_user(user_data.id)

    access_token = create_access_token(identity=user_data)
    response = redirect(
        url_for(
            "resources.redirect_route",
            **session.get("last_watched_endpoint", {}),
        )
    )
    set_access_cookies(response, access_token)
    return response


@auth_resource.route("/logout")
@jwt_required(optional=True)
def logout():
    jti = get_jwt().get("jti")
    if jti:
        now = datetime.now(timezone(timedelta(hours=+8)))
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()

    response = redirect("/")
    unset_jwt_cookies(response)
    return response


@auth_resource.route("/me", methods=["GET"])
@jwt_required(remember_endpoint=True)
def my_info():
    return {
        "id": current_user.user.id,
        "username": current_user.user.username,
        "email": current_user.user.email,
        "role": current_user.user.role.name,
        "lineId": current_user.user.line_id,
    }
