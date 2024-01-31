# -.- coding: utf-8 -.-
import os
from enum import Enum, auto
import requests
from excerpt import Excerpt
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

class HTTPMethod(Enum):
    GET = auto()
    POST = auto()
    PATCH = auto()
    DELETE = auto()

class RequestAPI:
    BASE_URL = "https://mylesmoylan.net/excerpts"
    LIST_URL = f"{BASE_URL}/json"

    def __init__(self) -> None:
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        if not username or not password:
            raise ValueError("Environment variables for USERNAME and PASSWORD must be set")
        self.auth = HTTPBasicAuth(username, password)

    def _make_request(self, method: HTTPMethod, url: str, use_auth: bool = True, **kwargs) -> dict:
        auth = self.auth if use_auth else None
        try:
            response = requests.request(method.name, url, auth=auth, **kwargs)
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP Error: {e.response.status_code} - {e.response.reason}") from e
        except requests.exceptions.RequestException as e:
            raise Exception("Connection Error") from e

    def list_excerpts(self) -> List[Excerpt]:
        """Retrieve a list of excerpts from the API."""
        excerpts_data = self._make_request(HTTPMethod.GET, self.LIST_URL, use_auth=False)
        return [Excerpt(e["id"], e["author"], e["work"], e["body"]) for e in excerpts_data.get("excerpts", [])]

    def _publish_or_update_excerpt(self, method: HTTPMethod, id: Optional[str] = None, author: str = "", work: str = "", body: str = "") -> dict:
        """Helper function to either publish a new excerpt or update an existing one."""
        url = self.BASE_URL if method == HTTPMethod.POST else f"{self.BASE_URL}/{id}"
        data = {"author": author, "work": work, "body": body}
        return self._make_request(method, url, json=data)

    def publish_excerpt(self, author: str, work: str, body: str) -> dict:
        """Publish a new excerpt."""
        return self._publish_or_update_excerpt(HTTPMethod.POST, author=author, work=work, body=body)

    def update_excerpt(self, id: str, author: str, work: str, body: str) -> dict:
        """Update an existing excerpt."""
        return self._publish_or_update_excerpt(HTTPMethod.PATCH, id=id, author=author, work=work, body=body)

    def delete_excerpt(self, id: str) -> dict:
        """Delete an existing excerpt."""
        return self._make_request(HTTPMethod.DELETE, f"{self.BASE_URL}/{id}")
