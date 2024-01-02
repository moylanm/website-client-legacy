# -.- coding: utf-8 -.-
import os
import requests
from excerpts import Excerpt
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

class RequestAPI:
    BASE_URL = "https://mylesmoylan.net/excerpts"
    LIST_URL = f"{BASE_URL}/json"

    def __init__(self) -> None:
        self.auth = HTTPBasicAuth(os.getenv("USERNAME"), os.getenv("PASSWORD"))

    def _make_request(self, method, url, **kwargs):
        response = requests.request(method, url, auth=self.auth, **kwargs)
        response.raise_for_status()
        return response.json()

    def list_excerpts(self) -> list[Excerpt]:
        excerpts = self._make_request("GET", self.LIST_URL)["excerpts"]
        return [Excerpt(e["id"], e["author"], e["work"], e["body"]) for e in excerpts]

    def _publish_or_update_excerpt(self, method, id=None, author="", work="", body=""):
        url = self.BASE_URL if method == "POST" else f"{self.BASE_URL}/{id}"
        data = {"author": author, "work": work, "body": body}
        return self._make_request(method, url, json=data)

    def publish_excerpt(self, author: str, work: str, body: str) -> str:
        return str(self._publish_or_update_excerpt("POST", author=author, work=work, body=body))

    def update_excerpt(self, id: str, author: str, work: str, body: str) -> str:
        return str(self._publish_or_update_excerpt("PATCH", id=id, author=author, work=work, body=body))

    def delete_excerpt(self, id: str) -> str:
        return str(self._make_request("DELETE", f"{self.BASE_URL}/{id}"))
