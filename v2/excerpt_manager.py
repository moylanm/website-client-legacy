from api import RequestAPI
from excerpt import Excerpt

class ExcerptManager:
    def __init__(self,):
        self.api = RequestAPI()

    def _process_response(self, response):
        match response:
            case {"status_code": status} if 200 <= status < 300:
                return {"success": True, "message": response["data"].get("message", "Operation successful")}

            case {"status_code": status} if status == 422:
                errors = response["data"].get("errors", "Validation error")
                
                if isinstance(errors, dict):
                    errors = "\n".join([f"{field}: {message}" for field, message in errors.items()])

                return {"success": False, "message": errors}
            
            case {"status_code": status}:
                return {"success": False, "message": response["data"].get("error", "Operation failed")}

            case _:
                return {"success": False, "message": "Unknown response format"}

    def publish_excerpt(self, author, work, body):
        response = self.api.publish_excerpt(author, work, body)
        return self._process_response(response)

    def update_excerpt(self, excerpt_id, author, work, body):
        response = self.api.update_excerpt(excerpt_id, author, work, body)
        return self._process_response(response)

    def delete_excerpt(self, excerpt_id):
        response = self.api.delete_excerpt(excerpt_id)
        return self._process_response(response)

    def list_excerpts(self):
        response = self.api.list_excerpts()
        return [Excerpt(e["id"], e["author"], e["work"], e["body"]) for e in response["data"].get("excerpts", [])]
