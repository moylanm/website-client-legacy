# -.- coding: utf-8 -.-
from PySide6.QtWidgets import QMessageBox

def parse_response(response_data: dict) -> str:
    if "message" in response_data:
        return response_data["message"]
    elif "error" in response_data:
        return response_data["error"]
    elif "errors" in response_data:
        return "\n".join([f"{field}: {message}" for field, message in response_data["errors"].items()])
    else:
        return "Unknown response format"

def dialog_box(text: str) -> QMessageBox:
    db = QMessageBox()
    db.setInformativeText(text)
    db.setStandardButtons(QMessageBox.StandardButton.Ok)
    return db
