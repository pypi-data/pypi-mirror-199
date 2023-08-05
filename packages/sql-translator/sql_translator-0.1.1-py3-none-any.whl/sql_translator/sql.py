import requests
from requests import Response


class Sql:
    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key
        self.__OPENAI_API_URL = "https://api.openai.com/v1/completions"

    @property
    def api_key(self) -> str:
        return self.__api_key

    @property
    def open_api_url(self) -> str:
        return self.__OPENAI_API_URL

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _parse_response(self, response: Response) -> str:
        return response.json()["choices"][0]["text"].strip()

    def _request(self, message: str, prompt: str) -> str:
        json = {
            "prompt": f"{prompt}\n\n{message}\n\nSQL Query:",
            "temperature": 0.5,
            "max_tokens": 2048,
            "n": 1,
            "stop": "\n",
            "model": "text-davinci-003",
            "frequency_penalty": 0.5,
            "presence_penalty": 0.5,
            "logprobs": 10,
        }
        response = requests.post(
            url=self.open_api_url, headers=self.headers, json=json
        )
        if response.status_code != 200:
            return response.json()
        return self._parse_response(response)

    def translator(self, message: str) -> str:
        sql = self._request(
            message=message,
            prompt="Translate this SQL query into natural language:",
        )
        return sql
