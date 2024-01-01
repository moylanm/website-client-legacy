# -.- coding: utf-8 -.-
import os, requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

class Excerpt:

    def __init__(self, id, author, work, body):
        self.id = id
        self.author = author
        self.work = work
        self.body = body

    def __str__(self):
        return f"{self.author} - {self.work}"

class RequestHandler:

    PUBLISH_URL = "https://mylesmoylan.net/excerpts"
    LIST_URL = "https://mylesmoylan.net/json/excerpts"

    def __init__(self):
        self.auth = HTTPBasicAuth(str(os.getenv("USERNAME")), str(os.getenv("PASSWORD")))

    def list_excerpts(self):
        res = requests.get(self.LIST_URL, auth=self.auth)
        return [Excerpt(e["id"], e["author"], e["work"], e["body"]) for e in res.json()["excerpts"]]

    def publish_excerpt(self, author, work, body):
        data = {"author": author, "work": work, "body": body}
        res = requests.post(self.PUBLISH_URL, auth=self.auth, json=data)
        return res.json()

    def update_excerpt(self, id, author, work, body):
        data = {"id": id, "author": author, "work": work, "body": body}
        res = requests.patch(f"{self.PUBLISH_URL}/{id}", auth=self.auth, json=data)
        return res.json()

    def delete_excerpt(self, id):
        res = requests.delete(f"{self.PUBLISH_URL}/{id}", auth=self.auth)
        return res.json()
