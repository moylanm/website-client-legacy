# -.- coding: utf-8 -.-
import re
from PySide6.QtWidgets import QMessageBox

MESSAGE_RX = re.compile(r"'([\w\s]*)'\s*:\s*'([\w\s]*)'")

def parse_response(res):
    m = re.search(MESSAGE_RX, res)
    return m[2] if m is not None else "could not parse response"

def dialog_box(text):
    db = QMessageBox()
    db.setInformativeText(text)
    db.setStandardButtons(QMessageBox.StandardButton.Ok)
    return db
