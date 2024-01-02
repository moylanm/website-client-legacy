# -.- coding: utf-8 -.-
import sys

from api import RequestAPI
from helpers import dialog_box, parse_response
from PySide6.QtCore import QRect, Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTextEdit,
    QWidget
)

API = RequestAPI()

SUCCESS_RESPONSE = {
    "publish": "excerpt successfully created",
    "update": "excerpt successfully updated",
    "delete": "excerpt successfully deleted"
}

class Main(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Website Client")
        self.resize(800, 600)
        self.excerpts = []
        self.edit_window = None
        self.init_ui()

    def init_ui(self):
        self.create_tabs()
        self.create_publish_tab()
        self.create_edit_tab()
        self.load_excerpts()

    def create_tabs(self):
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(QRect(0, 0, 800, 590))
        self.publish_tab = QWidget()
        self.edit_tab = QWidget()
        self.tab_widget.addTab(self.publish_tab, "Publish")
        self.tab_widget.setTabText(0, "Publish")
        self.tab_widget.addTab(self.edit_tab, "Edit")
        self.tab_widget.setTabText(1, "Edit")
        self.tab_widget.setCurrentIndex(0)

    def create_publish_tab(self):
        labels = ["Author :", "Work :", "Body :"]
        fields = [QLineEdit, QLineEdit, QTextEdit]
        positions = [(15, 10), (25, 50), (25, 88)]

        for label, field, pos in zip(labels, fields, positions):
            name = label.lower().replace(' :', '')
            setattr(self, f"{name}_label", QLabel(self.publish_tab))
            getattr(self, f"{name}_label").setText(label)
            getattr(self, f"{name}_label").setGeometry(pos[0], pos[1], 60, 30)

            setattr(self, f"{name}_field", field(self.publish_tab))
            getattr(self, f"{name}_field").setGeometry(70, pos[1], 690, 30 if field == QLineEdit else 370)

        self.publish_button = QPushButton(self.publish_tab)
        self.publish_button.setText("Publish")
        self.publish_button.setGeometry(QRect(640, 465, 120, 40))
        self.publish_button.clicked.connect(self.publish)

        self.clear_button = QPushButton(self.publish_tab)
        self.clear_button.setText("Clear")
        self.clear_button.setGeometry(510, 465, 120, 40)
        self.clear_button.clicked.connect(self.clear)

    def create_edit_tab(self):
        self.load_excerpts()

    def publish(self):
        response = API.publish_excerpt(
            self.author_field.text(),
            self.work_field.text(),
            self.body_field.toPlainText()
        )

        message = parse_response(response)

        db = dialog_box(message)
        db.exec()

        if message == SUCCESS_RESPONSE["publish"]:
            self.clear()
            self.load_excerpts()

        db.close()

    def clear(self):
        for field in ["author", "work", "body"]:
            getattr(self, f"{field}_field").setText("")

    def load_excerpts(self):
        self.excerpts = API.list_excerpts()

        self.table = QTableWidget(len(self.excerpts), 1, self.edit_tab)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.resize(800, 560)

        for row, excerpt in enumerate(self.excerpts):
            button = QPushButton(str(excerpt))
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.clicked.connect(self.on_clicked(excerpt))
            self.table.setCellWidget(row, 0, button)

        self.table.show()

    def on_clicked(self, excerpt):
        def new_edit_window():
            self.edit_window = EditWindow(excerpt, parent=self)
            self.edit_window.edit_event.connect(self.load_excerpts)
            self.edit_window.show()

        return new_edit_window

class EditWindow(QMainWindow):

    edit_event = Signal()

    def __init__(self, excerpt, parent=None):
        super().__init__(parent)
        self.excerpt_id = excerpt.id
        self.setWindowTitle(str(excerpt))
        self.resize(800, 600)
        self.init_ut(excerpt)

    def init_ut(self, excerpt):
        self.create_labels()
        self.create_fields(excerpt)
        self.create_buttons()

    def create_labels(self):
        labels_data = [
            ("Author :", 15, 10),
            ("Work :", 25, 50),
            ("Body :", 25, 88),
        ]

        for label_text, x, y in labels_data:
            label = QLabel(self)
            label.setText(label_text)
            label.setGeometry(QRect(x, y, 60, 30))

    def create_fields(self, excerpt):
        fields_data = [
            (QLineEdit, excerpt.author, 70, 10),
            (QLineEdit, excerpt.work, 70, 50),
            (QTextEdit, excerpt.body, 70, 90),
        ]

        for field_type, field_value, x, y in fields_data:
            field = field_type(self)
            field.setGeometry(QRect(x, y, 690, 30 if field_type == QLineEdit else 370))
            field.setText(str(field_value))
            setattr(self, f"{field_type.__name__.lower()}_{y}", field)

    def create_buttons(self):
        buttons_data = [
            ("Update", self.update_excerpt, 640, 465),
            ("Delete", self.delete_excerpt, 510, 465),
        ]

        for button_text, handler, x, y in buttons_data:
            button = QPushButton(self)
            button.setText(button_text)
            button.setGeometry(QRect(x, y, 120, 40))
            button.clicked.connect(handler)

    def update_excerpt(self):
        response = API.update_excerpt(
            self.excerpt_id,
            self.get_field_text(QLineEdit, 10),
            self.get_field_text(QLineEdit, 50),
            self.get_field_text(QTextEdit, 90)
        )

        self.handle_response(response, "update")

    def delete_excerpt(self):
        mb = QMessageBox()
        mb.setInformativeText("Are you sure you want to delte this excerpt?")
        mb.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        ret = mb.exec()

        if ret == QMessageBox.StandardButton.Yes:
            mb.close()
            response = API.delete_excerpt(self.excerpt_id)
            self.handle_response(response, "delete")
        else:
            mb.close()

    def handle_response(self, response, action):
        message = parse_response(response)
        db = dialog_box(message)
        db.exec()

        if message == SUCCESS_RESPONSE[action]:
            self.edit_event.emit()
            self.close()

        db.close()

    def get_field_text(self, field_type, y):
        field = getattr(self, f"{field_type.__name__.lower()}_{y}")
        return field.text() if field_type == QLineEdit else field.toPlainText()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()

    main.show()
    sys.exit(app.exec())
