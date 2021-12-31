import json
from google.cloud import dialogflow
from google.protobuf.json_format import MessageToJson
from typing import Any

from settings import language_code, project_id


class DialogflowClient:
    client: dialogflow.SessionsClient

    def __init__(self):
        self.client = dialogflow.SessionsClient()

    def detect_intent(
        self, session_id: str, text: str, event: bool
    ) -> dict[str, Any]:
        session = self.client.session_path(project_id, session_id)

        if event:
            event_input = dialogflow.EventInput(
                name=text, language_code=language_code
            )
            query_input = dialogflow.QueryInput(event=event_input)
        else:
            text_input = dialogflow.TextInput(
                text=text, language_code=language_code
            )
            query_input = dialogflow.QueryInput(text=text_input)

        response = self.client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        json_response = MessageToJson(response._pb)
        dict_response = json.loads(json_response)

        return dict_response["queryResult"]
