# -.- coding: utf-8 -.-
from PySide6.QtWidgets import QMessageBox

def parse_response(response_data: dict) -> str:
    match response_data:
        case {"message": message}:
            return message
        case {"error": error}:
            return error
        case {"errors": errors} if isinstance(errors, dict):
            return "\n".join([f"{field}: {message}" for field, message in errors.items()])
        case _:
            return "Unknown response format"

def dialog_box(text: str) -> QMessageBox:
    db = QMessageBox()
    db.setInformativeText(text)
    db.setStandardButtons(QMessageBox.StandardButton.Ok)
    return db
