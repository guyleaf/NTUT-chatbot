import json
import requests
from linebot import LineBotApi

from settings import (
    line_api_base_url,
    richmenu_for_seller_json_path,
    richmenu_for_seller_image_path,
    richmenu_for_customer_json_path,
    richmenu_for_customer_image_path,
    web_url,
)


class RichMenu:
    def __init__(self, line_bot_api: LineBotApi, channel_access_token: str):
        self.line_bot_api = line_bot_api
        self.headers = {
            "Authorization": "Bearer {}".format(channel_access_token)
        }

    def _get_richmenu(self, is_customer: bool):
        json_path = (
            richmenu_for_customer_json_path
            if is_customer
            else richmenu_for_seller_json_path
        )
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _prepare_json(self, data: dict):
        for area in data["areas"]:
            if area["action"]["type"] == "uri":
                uri = web_url + area["action"]["uri"]

                if "data" in area["action"].keys():
                    uri = uri + area["action"]["data"]

                area["action"]["uri"] = uri

    def create(self, line_id, is_customer: bool = True):
        data = self._get_richmenu(is_customer)
        self._prepare_json(data)

        richmenu_id = self.upload_menu_data(data)
        self.upload_menu_image(richmenu_id, is_customer)
        self.update_user_menu(line_id, richmenu_id)

    def upload_menu_data(self, data):
        response = requests.post(
            f"{line_api_base_url}richmenu",
            json=data,
            headers=self.headers,
        )

        return json.loads(response.text)["richMenuId"]

    def upload_menu_image(self, richmenu_id, is_customer):
        richmenu_image_path = (
            richmenu_for_customer_image_path
            if is_customer
            else richmenu_for_seller_image_path
        )
        with open(richmenu_image_path, "rb") as f:
            content_type = "image/{}".format(
                richmenu_image_path.split(".")[-1]
            )
            self.line_bot_api.set_rich_menu_image(richmenu_id, content_type, f)

    def update_user_menu(self, line_id, richmenu_id):
        requests.post(
            f"{line_api_base_url}user/" + line_id + "/richmenu/" + richmenu_id,
            headers=self.headers,
        )
