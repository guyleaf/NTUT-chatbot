import requests
import json
from typing import Any

from app import line_bot_api, richmenu, logger
from helpers import get_text_send_message_object
from settings import web_url
from messages import (
    register_handle_message,
    register_success_message,
    register_failure_message,
    welcome_message_for_registered,
    functional_explain_message_for_customer,
    functional_explain_message_for_admin,
)


class DialogflowHandler:
    def _register_user(self, line_id: str, user_name: str):
        request_body = {"line_id": line_id, "name": user_name}
        # TODO: Add auth api key
        response = requests.post(web_url + "/register", json=request_body)
        user = json.loads(response.content)
        return user, 200

    def _handle_register_action(self, response: dict[str, Any], line_id: str):
        user_name = response["parameters"]["person"]["name"]

        logger.info("registering user...")
        line_bot_api.push_message(line_id, register_handle_message)

        if len(user_name) == 0:
            line_bot_api.push_message(line_id, register_failure_message)
            return

        # send register request
        user, status_code = self._register_user(line_id, user_name)

        if status_code == 200:
            user_id = user["id"]
            user_name = user["name"]
            is_admin = user["is_admin"]

            messages = [
                register_success_message,
                get_text_send_message_object(
                    welcome_message_for_registered.format(
                        "管理員" if is_admin else "顧客", user_name
                    )
                ),
                get_text_send_message_object(
                    functional_explain_message_for_admin
                    if is_admin
                    else functional_explain_message_for_customer
                ),
            ]

            line_bot_api.push_message(line_id, messages)
            richmenu.create(line_id, user_id, is_admin)
        else:
            line_bot_api.push_message(line_id, register_failure_message)

    def _handle_fulfillment_messages(
        self, messages: list[dict[str, Any]], line_id: str
    ):
        for message in messages:
            message = get_text_send_message_object(message["text"]["text"][0])
            line_bot_api.push_message(line_id, message)

    def handle_query_response(self, response: dict[str, Any], line_id: str):
        logger.info("handling query response...")

        if "action" in response and response["action"] == "registerAction":
            self._handle_register_action(response, line_id)
        elif response["fulfillmentMessages"]:
            self._handle_fulfillment_messages(
                response["fulfillmentMessages"], line_id
            )
