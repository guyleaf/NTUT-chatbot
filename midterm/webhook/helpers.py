from linebot.models import TextSendMessage


def get_text_send_message_object(text: str):
    return TextSendMessage(text=text)
