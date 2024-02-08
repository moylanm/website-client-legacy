# -.- coding: utf-8 -.-
import os
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from dotenv import load_dotenv
from typing import Any, Dict

load_dotenv()

class RequestAPIException(Exception):
    def __init__(self, message="API Request Error", original_exception=None):
        super().__init__(f"{message}: {str(original_exception)}")

class RequestAPI:
    def __init__(self) -> None:
        self.base_url = os.getenv("BASE_URL")
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")

        if not username or not password or not self.base_url:
            raise ValueError("Environment variables must be set")

        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)

    def _make_request(self, method: str, endpoint: str, use_auth: bool = True, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        auth = self.session.auth if use_auth else None
        try:
            response = self.session.request(method, url, auth=auth, **kwargs)
            return {
                "status_code": response.status_code,
                "data": response.json()
            }
        except RequestException as e:
            raise RequestAPIException(original_exception=e)
        except ValueError as e:
            raise RequestAPIException(message="Invalid JSON response", original_exception=e)

    def list_excerpts(self) -> Dict[str, Any]:
        return self._make_request("GET", "json", use_auth=False)

    def publish_excerpt(self, author: str, work: str, body: str) -> Dict[str, Any]:
        data = {"author": author, "work": work, "body": body}
        return self._make_request("POST", "", json=data)

    def update_excerpt(self, id: str, author: str, work: str, body: str) -> Dict[str, Any]:
        data = {"author": author, "work": work, "body": body}
        return self._make_request("PATCH", id, json=data)

    def delete_excerpt(self, id: str) -> Dict[str, Any]:
        return self._make_request("DELETE", id)

    def close(self) -> None:
        self.session.close()
