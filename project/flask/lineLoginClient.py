from typing import Any
from authlib.integrations.base_client.errors import OAuthError

from authlib.integrations.flask_client import OAuth
from authlib.jose import JsonWebToken
from authlib.oidc.core import CodeIDToken
from authlib.common.security import generate_token

from flask import session, current_app
from flask.app import Flask


class LineLoginClient:
    _CLIENT_ID: str
    _CLIENT_SECRET: str
    _jwt: JsonWebToken
    _oauth: OAuth

    _claims_options: "dict[str, Any]"

    def __init__(self, app: Flask):
        self._CLIENT_ID = app.config["LINE_CLIENT_ID"]
        self._CLIENT_SECRET = app.config["LINE_CLIENT_SECRET"]
        oauth = OAuth(app)
        oauth.register(
            name="line",
            authorize_url="https://access.line.me/oauth2/v2.1/authorize",
            access_token_url="https://api.line.me/oauth2/v2.1/token",
            client_kwargs={
                "scope": "openid profile email",
                "token_endpoint_auth_method": "client_secret_post",
            },
        )

        self._jwt = JsonWebToken(["HS256"])
        self._oauth = oauth
        self._claims_options = {
            "iss": {"essential": True, "value": "https://access.line.me"},
            "aud": {"essential": True, "value": self._CLIENT_ID},
        }

    @staticmethod
    def _generate_token() -> str:
        return generate_token()

    def _save_session(self, data: "dict[str, str]"):
        session["line_login"] = data

    def _get_session(self) -> "dict[str, str]":
        return session.pop("line_login", None)

    def authorize_redirect(self, redirect_uri: str):
        data = {
            "nonce": self._generate_token(),
            "state": self._generate_token(),
        }

        self._save_session(data)
        return self._oauth.line.authorize_redirect(redirect_uri, **data)

    def authorize_access_token(self):
        try:
            token = self._oauth.line.authorize_access_token()

            claims = self._jwt.decode(
                token["id_token"],
                self._CLIENT_SECRET,
                claims_cls=CodeIDToken,
                claims_options=self._claims_options,
                claims_params=self._get_session(),
            )
        except OAuthError as e:
            current_app.log_exception(e)
            return None

        claims.validate()
        return {
            "username": claims["name"],
            "lineId": claims["sub"],
        }
