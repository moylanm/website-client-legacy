# -.- coding: utf-8 -.-
from PySide6.QtWidgets import QMessageBox

def parse_response_dataponse(response_data: dict) -> str:
    try:
        if "message" in response_data:
            return response_data["message"]
        elif "error" in response_data:
            return response_data["error"]
        elif "errors" in response_data:
            errors = response_data["errors"]
            return "\n".join([f"{field}: {error}" for field, error in errors.items()])
        else:
            return "Unknown response_dataponse format"
    except Exception as e:
        return f"General error: {e}"

def dialog_box(text: str) -> QMessageBox:
    db = QMessageBox()
    db.setInformativeText(text)
    db.setStandardButtons(QMessageBox.StandardButton.Ok)
    return db
