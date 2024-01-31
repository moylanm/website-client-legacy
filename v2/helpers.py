# -.- coding: utf-8 -.-
import json
from PySide6.QtWidgets import QMessageBox

def parse_response(res: str) -> str:
    try:
        res = res.replace("\'", "\"")
        data = json.loads(res)

        if "message" in data:
            return data["message"]
        elif "error" in data:
            return data["error"]
        elif "errors" in data:
            errors = data["errors"]
            return "\n".join([f"{field}: {error}" for field, error in errors.items()])
        else:
            return "Unknown response format"

    except json.JSONDecodeError as e:
        return f"Error parsing response: {e}"
    except Exception as e:
        return f"General error: {e}"

def dialog_box(text: str) -> QMessageBox:
    db = QMessageBox()
    db.setInformativeText(text)
    db.setStandardButtons(QMessageBox.StandardButton.Ok)
    return db
