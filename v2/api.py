# -.- coding: utf-8 -.-
import os
import requests
from excerpt import Excerpt
from requests.auth import HTTPBasicAuth
from requests.exceptions import JSONDecodeError, HTTPError, RequestException
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional

load_dotenv()

class ConnectionErrorException(Exception):
    def __init__(self, message="Connection Error"):
        super().__init__(message)

class JSONDecodeErrorException(Exception):
    def __init__(self, message="Failed to decode JSON response"):
        super().__init__(message)

class RequestAPI:
    BASE_URL = "https://mylesmoylan.net/excerpts"
    LIST_URL = f"{BASE_URL}/json"

    def __init__(self) -> None:
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        if not username or not password:
            raise ValueError("Environment variables for USERNAME and PASSWORD must be set")
        self.auth = HTTPBasicAuth(username, password)

    def _make_request(self, method: str, url: str, use_auth: bool = True, **kwargs) -> Dict[str, Any]:
        auth = self.auth if use_auth else None
        try:
            response = requests.request(method.upper(), url, auth=auth, **kwargs)
            try:
                return response.json()
            except JSONDecodeError as e:
                raise JSONDecodeErrorException() from e
        except RequestException as e:
            raise ConnectionErrorException() from e

    def list_excerpts(self) -> List[Excerpt]:
        """Retrieve a list of excerpts from the API."""
        excerpts_data = self._make_request("GET", self.LIST_URL, use_auth=False)
        return [Excerpt(e["id"], e["author"], e["work"], e["body"]) for e in excerpts_data.get("excerpts", [])]

    def _publish_or_update_excerpt(self, method: str, id: Optional[str] = None, author: str = "", work: str = "", body: str = "") -> Dict[str, Any]:
        """Helper function to either publish a new excerpt or update an existing one."""
        url = self.BASE_URL if method == "POST" else f"{self.BASE_URL}/{id}"
        data = {"author": author, "work": work, "body": body}
        return self._make_request(method, url, json=data)

    def publish_excerpt(self, author: str, work: str, body: str) -> Dict[str, Any]:
        """Publish a new excerpt."""
        return self._publish_or_update_excerpt("POST", author=author, work=work, body=body)

    def update_excerpt(self, id: str, author: str, work: str, body: str) -> Dict[str, Any]:
        """Update an existing excerpt."""
        return self._publish_or_update_excerpt("PATCH", id=id, author=author, work=work, body=body)

    def delete_excerpt(self, id: str) -> Dict[str, Any]:
        """Delete an existing excerpt."""
        return self._make_request("DELETE", f"{self.BASE_URL}/{id}")
