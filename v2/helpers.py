# -.- coding: utf-8 -.-
import re
from PySide6.QtWidgets import QMessageBox

MESSAGE_RX = re.compile(r"'([^']*)'\s*:\s*'([^']*)'")

def parse_response(res: str) -> str:
    try:
        m = MESSAGE_RX.search(res)
        return m.group(2) if m else "could not parse response"
    except Exception as e:
        return f"Error parsing response: {e}"

def dialog_box(text: str) -> QMessageBox:
    db = QMessageBox()
    db.setInformativeText(text)
    db.setStandardButtons(QMessageBox.StandardButton.Ok)
    return db
