import json
import requests
from typing import Dict, List, Union


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.header = { "Content-Type": "application/json", "Accept": "*/*" }

    def set_header_param(self, header_key: str, header_val: str):
        self.header[header_key] = header_val

    def set_jwt_token_in_auth_header(self, token_path: str, username: str, password: str):
        res = requests.post(f"{self.base_url}{token_path}", json.dumps({ "username": username, "password": password }), headers=self.header)
        response_json = res.json()

        self.set_header_param("Authorization", f"Bearer {response_json['token']}")

    def get_data(self, path: str) -> Union[Dict, List[Dict]]:
        url = f"{self.base_url}{path}"
        response = requests.get(url, headers=self.header)
        return json.loads(response.text)
