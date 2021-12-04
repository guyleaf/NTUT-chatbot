import requests
import json
from typing import Any
from logging import getLogger

from app import line_bot_api, richmenu, firestore_dao
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

logger = getLogger("webhook")


class DialogflowHandler:
    def _register_member(self, line_id: str, user_name: str):
        request_body = {"lineId": line_id, "name": user_name}
        # TODO: Add auth api key
        response = requests.post(web_url + "/register", json=request_body)
        member = json.loads(response.content)
        return member

    def handle_query_response(self, response: dict[str, Any], line_id: str):
        logger.info("handling query response...")

        if "action" in response and response["action"] == "registerAction":
            member_name = response["parameters"]["person"]["name"]

            logger.info("registering member...")
            line_bot_api.push_message(line_id, register_handle_message)

            if len(member_name) == 0:
                line_bot_api.push_message(line_id, register_failure_message)
                return

            member = self._register_member(line_id, member_name)
            if member:
                user_id = member["id"]
                user_name = member["name"]
                user_role = firestore_dao.get_role_name(member["role_id"])
                is_admin = user_role == "管理員"

                messages = [
                    register_success_message,
                    get_text_send_message_object(
                        welcome_message_for_registered.format(
                            user_role, user_name
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

        if response["fulfillmentMessages"]:
            for message in response["fulfillmentMessages"]:
                message = get_text_send_message_object(
                    message["text"]["text"][0]
                )
                line_bot_api.push_message(line_id, message)
