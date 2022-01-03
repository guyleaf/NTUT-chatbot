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
)

from app import oauth_client
from models import User
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

    user_data = User.query.filter_by(line_id=user["lineId"]).first()

    # if user_data is None:
    #     access_token = create_access_token(
    #         identity=user["lineId"], fresh=True, additional_claims=user
    #     )
    # else:
    #     additional_claims = {
    #         "username": user_data.username,
    #         "lineId": user_data.line_id,
    #         "role": user_data.role.name,
    #     }
    #     access_token = create_access_token(
    #         identity=user_data.id, additional_claims=additional_claims
    #     )

    response = redirect(url_for("redirect_route", **get_redirect_data()))
    set_access_cookies(response, access_token)
    return response


@auth_resource.route("/logout")
def logout():
    response = redirect("/")
    unset_jwt_cookies(response)
    return response
