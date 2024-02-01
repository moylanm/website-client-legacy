# -.- coding: utf-8 -.-
import os
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from dotenv import load_dotenv
from typing import Any, Optional, Dict

load_dotenv()

class RequestAPIException(Exception):
    def __init__(self, message="API Request Error", original_exception=None):
        super().__init__(f"{message}: {str(original_exception)}")

class RequestAPI:
    BASE_URL = "https://mylesmoylan.net/excerpts"

    def __init__(self) -> None:
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        if not username or not password:
            raise ValueError("Environment variables for USERNAME and PASSWORD must be set")
        self.auth = HTTPBasicAuth(username, password)

    def _make_request(self, method: str, url: str, use_auth: bool = True, **kwargs) -> Dict[str, Any]:
        with requests.Session() as session:
            session.auth = self.auth if use_auth else None
            try:
                response = session.request(method, url, **kwargs)
                return {
                    "status_code": response.status_code,
                    "data": response.json()
                }
            except RequestException as e:
                raise RequestAPIException(original_exception=e)

    def list_excerpts(self) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/json"
        return self._make_request("GET", url, use_auth=False)

    def _publish_or_update_excerpt(self, method: str, author: str, work: str, body: str, id: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{id}" if id else self.BASE_URL
        data = {"author": author, "work": work, "body": body}
        return self._make_request(method, url, json=data)

    def publish_excerpt(self, author: str, work: str, body: str) -> Dict[str, Any]:
        return self._publish_or_update_excerpt("POST", author=author, work=work, body=body)

    def update_excerpt(self, id: str, author: str, work: str, body: str) -> Dict[str, Any]:
        return self._publish_or_update_excerpt("PATCH", author=author, work=work, body=body, id=id)

    def delete_excerpt(self, id: str) -> Dict[str, Any]:
        return self._make_request("DELETE", f"{self.BASE_URL}/{id}")
