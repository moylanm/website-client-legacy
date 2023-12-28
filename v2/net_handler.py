import requests


class Excerpt:

    def __init__(self, id, author, work, body):
        self.id = id
        self.author = author
        self.work = work
        self.body = body

    def __str__(self):
        return f"{self.author} - {self.work}"

class NetHandler:

    PUBLISH_URL = "https://mylesmoylan.net/excerpts"
    LIST_URL = "https://mylesmoylan.net/json/excerpts"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def list_excerpts(self):
        req = requests.get(self.LIST_URL, auth=(self.username, self.password))
        return [Excerpt(e["id"], e["author"], e["work"], e["body"]) for e in req.json()["excerpts"]]

    def publish_excerpt(self, excerpt):
        pass

    def update_excerpt(self, excerpt):
        pass

    def delete_excerpt(self, id):
        pass
