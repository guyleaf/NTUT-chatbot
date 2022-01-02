﻿from flask import session


def save_redirect_data(endpoint: str):
    session["redirect_data"] = {"page": endpoint}


def get_redirect_data() -> dict:
    return session.pop("redirect_data", {})
