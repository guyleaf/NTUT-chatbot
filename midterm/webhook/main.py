from linebot.models import (
    FollowEvent,
    MessageEvent,
    TextMessage,
    PostbackEvent,
)
from logging import getLogger

from app import (
    webhook_handler,
    line_bot_api,
)
from dialogflow.dialogflowClient import DialogflowClient
from dialogflow.dialogflowHandler import DialogflowHandler
from messages import welcome_message, error_message

logger = getLogger("webhook")
dialogflow_client = DialogflowClient()
dialogflow_handler = DialogflowHandler()


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

    line_bot_api.reply_message(reply_token, welcome_message)

    logger.info("detecting intent from follow event")
    response = dialogflow_client.detect_intent(line_id, "followEvent", True)
    dialogflow_handler.handle_query_response(response, line_id)


@webhook_handler.add(PostbackEvent)
def handle_postback(event: PostbackEvent):
    reply_token = event.reply_token
    reply_messages = [error_message]
    line_bot_api.reply_message(reply_token, reply_messages)


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    line_id = event.source.user_id
    text = event.message.text

    logger.info("detecting intent from message event")
    response = dialogflow_client.detect_intent(line_id, text, False)
    dialogflow_handler.handle_query_response(response, line_id)
