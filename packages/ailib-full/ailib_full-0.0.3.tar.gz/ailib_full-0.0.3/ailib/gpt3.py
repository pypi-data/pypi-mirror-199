import requests
from typing import List

api_key = "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"

class Model:
    def __init__(self, model_id: str, object: str, owned_by: str):
        self.model_id: str = model_id
        self.object: str = object
        self.owned_by: str = owned_by

    def __repr__(self) -> str:
        return f"Model(model_id:'{self.model_id}', object:'{self.object}', owned_by:'{self.owned_by}')"

class Models:
    @staticmethod
    def list() -> List[Model]:
        response = requests.get("https://api.openai.com/v1/models", headers={'Authorization': f'Bearer {api_key}'})
        json = response.json()

        models = []

        for model in json['data']:
            models.append(Model(model['id'], model['object'], model['owned_by']))

        return models

class TextCompletion:
    @staticmethod
    def create(model: str, prompt: str) -> str:
        pass