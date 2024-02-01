# -.- coding: utf-8 -.-
from api import RequestAPI
from excerpt import Excerpt
from typing import Any, Dict, List

HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_UNPROCESSABLE_ENTITY = 422

class ExcerptManager:
    def __init__(self,):
        self.api = RequestAPI()

    def _process_response(self, response: Dict) -> Dict[str, Any]:
        match response:
            case {"status_code": status} if status in [HTTP_STATUS_OK, HTTP_STATUS_CREATED]:
                return {"success": True, "message": response["data"].get("message", "Operation successful")}

            case {"status_code": status, "data": data} if status == HTTP_STATUS_UNPROCESSABLE_ENTITY:
                errors = data.get("errors", "Validation error")
                
                if isinstance(errors, dict):
                    errors = "\n".join([f"{field}: {message}" for field, message in errors.items()])

                return {"success": False, "message": errors}
            
            case {"status_code": _}:
                return {"success": False, "message": response["data"].get("error", "Operation failed")}

            case _:
                return {"success": False, "message": "Unknown response format"}

    def publish_excerpt(self, author: str, work: str, body: str) -> Dict[str, Any]:
        response = self.api.publish_excerpt(author, work, body)
        return self._process_response(response)

    def update_excerpt(self, excerpt_id: str, author: str, work: str, body: str) -> Dict[str, Any]:
        response = self.api.update_excerpt(excerpt_id, author, work, body)
        return self._process_response(response)

    def delete_excerpt(self, excerpt_id: str) -> Dict[str, Any]:
        response = self.api.delete_excerpt(excerpt_id)
        return self._process_response(response)

    def list_excerpts(self) -> List[Excerpt]:
        response = self.api.list_excerpts()

        if response["status_code"] != HTTP_STATUS_OK:
            return []
        
        return [Excerpt(e["id"], e["author"], e["work"], e["body"]) for e in response["data"].get("excerpts", [])]
