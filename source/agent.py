from source.api_methods import get_model_data
import json

class Agent(object):
    def __init__(self, secrets: dict, agent_type: list):
        self.secrets = secrets
        self.agent_type = agent_type

    def run_model(self, messages: list, token: str, model: str) -> str:
        """
        Method returns user input and model result
        :return: model response
        """
        prompt_payload = json.dumps({
            "model": model,
            "messages": self.agent_type + messages,
            "stream": False,
            "update_interval": 0
        })
        prompt_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        response, status = get_model_data(
            url=self.secrets['model_answer_api']['url']
            , payload=prompt_payload
            , headers=prompt_headers
            , method="POST"
        )
        if status == 200:
            return './/.'.join([x['message']['content'] for x in response.json()['choices']])
        else:
            return ''