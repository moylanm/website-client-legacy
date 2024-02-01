# -.- coding: utf-8 -.-
class Excerpt:

    def __init__(self, id, author, work, body):
        self.id = id
        self.author = author
        self.work = work
        self.body = body

    def __str__(self):
        return f"{self.author} - {self.work}"
