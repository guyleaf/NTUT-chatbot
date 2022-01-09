from linebot.models import FollowEvent

from app import webhook_handler, line_bot_api, logger, richmenu

# from dialogflow.dialogflowClient import DialogflowClient
# from dialogflow.dialogflowHandler import DialogflowHandler
from messages import (
    welcome_message,
    register_message,
    functional_explain_message_for_customer,
    functional_explain_message_for_others,
    registered_message,
)

import cloudSqlClient as cloudSql


# dialogflow_client = DialogflowClient()
# dialogflow_handler = DialogflowHandler()


def main(request):
    # get X-Line-Signature header value
    signature = request.headers.get("X-Line-Signature")

    if signature is None:
        return "400 BadRequest", 400

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        logger.info("*** handling request ***")
        webhook_handler.handle(body, signature)
    except Exception as e:
        logger.exception(e)
        return "500 Server Error", 500

    logger.info("*** end request ***")
    return "200 OK"


@webhook_handler.add(FollowEvent)
def handle_follow(event: FollowEvent):
    line_id = event.source.user_id
    reply_token = event.reply_token

    user = cloudSql.find_user(line_id)
    if user:
        line_bot_api.reply_message(reply_token, welcome_message)
        is_customer = user.role.name == "customer"
        functional_explain_message = (
            functional_explain_message_for_customer
            if is_customer
            else functional_explain_message_for_others
        )

        if user.role.name == "admin":
            role_name = "系統管理員"
        elif user.role.name == "seller":
            role_name = "管理員"
        else:
            role_name = "顧客"

        line_bot_api.push_message(
            line_id, registered_message.format(role_name, user.username)
        )
        line_bot_api.push_message(line_id, functional_explain_message)
        richmenu.create(line_id, is_customer)
    else:
        line_bot_api.reply_message(reply_token, register_message)

    # logger.info("detecting intent from follow event")
    # response = dialogflow_client.detect_intent(line_id, "followEvent", True)
    # dialogflow_handler.handle_query_response(response, line_id)


# @webhook_handler.add(MessageEvent, message=TextMessage)
# def handle_message(event: MessageEvent):
#     line_id = event.source.user_id
#     text = event.message.text

#     logger.info("detecting intent from message event")
#     response = dialogflow_client.detect_intent(line_id, text, False)
#     dialogflow_handler.handle_query_response(response, line_id)
