# -.- coding: utf-8 -.-
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QLabel, QLineEdit, QMessageBox, QTextEdit

SUCCESS_RESPONSE = {
    "publish": "excerpt successfully created",
    "update": "excerpt successfully updated",
    "delete": "excerpt successfully deleted"
}

FORM_METADATA = [
    {"label": "Author :", "label_geometry": QRect(15, 10, 60, 30), "field_type": QLineEdit, "field_geometry": QRect(70, 10, 690, 30), "field_name": "author_field", "attr": "author"},
    {"label": "Work :", "label_geometry": QRect(25, 50, 60, 30), "field_type": QLineEdit, "field_geometry": QRect(70, 50, 690, 30), "field_name": "work_field", "attr": "work"},
    {"label": "Body :", "label_geometry": QRect(25, 88, 60, 30), "field_type": QTextEdit, "field_geometry": QRect(70, 88, 690, 370), "field_name": "body_field", "attr": "body"}
]

def create_form_fields(parent, excerpt=None):
    for el in FORM_METADATA:
        label = QLabel(el["label"], parent)
        label.setGeometry(el["label_geometry"])

        field = el["field_type"](parent)
        field.setGeometry(el["field_geometry"])

        if excerpt is not None:
            field.setText(getattr(excerpt, el["attr"], ""))

        setattr(parent, el["field_name"], field)

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
