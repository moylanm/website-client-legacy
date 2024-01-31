from helpers import parse_response

class ExcerptManager:
    def __init__(self, api):
        self.api = api

    def publish_excerpt(self, author, work, body):
        response = self.api.publish_excerpt(author, work, body)
        return parse_response(response)

    def update_excerpt(self, excerpt_id, author, work, body):
        response = self.api.update_excerpt(excerpt_id, author, work, body)
        return parse_response(response)

    def delete_excerpt(self, excerpt_id):
        response = self.api.delete_excerpt(excerpt_id)
        return parse_response(response)

    def list_excerpts(self):
        return self.api.list_excerpts()
