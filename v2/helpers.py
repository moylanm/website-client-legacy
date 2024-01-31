# -.- coding: utf-8 -.-
from PySide6.QtWidgets import QMessageBox

def parse_response(res: dict) -> str:
    try:
        if "message" in res:
            return res["message"]
        elif "error" in res:
            return res["error"]
        elif "errors" in res:
            errors = res["errors"]
            return "\n".join([f"{field}: {error}" for field, error in errors.items()])
        else:
            return "Unknown response format"
    except Exception as e:
        return f"General error: {e}"

def dialog_box(text: str) -> QMessageBox:
    db = QMessageBox()
    db.setInformativeText(text)
    db.setStandardButtons(QMessageBox.StandardButton.Ok)
    return db
