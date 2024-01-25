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

class MainUI(QMainWindow):

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.excerpts = []
        self.setup_window()
        self.init_ui()

    def setup_window(self):
        self.setWindowTitle("Website Client")
        self.resize(800, 600)

    def init_ui(self):
        self.create_tabs()
        self.setup_publish_tab()
        self.setup_edit_tab()

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

    def setup_publish_tab(self):
        create_form_fields(self.publish_tab)

        publish_button = QPushButton(self.publish_tab)
        publish_button.setText("Publish")
        publish_button.setGeometry(QRect(640, 465, 120, 40))
        publish_button.clicked.connect(self.publish_excerpt)

        clear_button = QPushButton(self.publish_tab)
        clear_button.setText("Clear")
        clear_button.setGeometry(510, 465, 120, 40)
        clear_button.clicked.connect(self.clear_form)

    def setup_edit_tab(self):
        self.edit_window = None
        self.load_excerpts()

    def publish_excerpt(self):
        response = API.publish_excerpt(
            self.publish_tab.author_field.text(),
            self.publish_tab.work_field.text(),
            self.publish_tab.body_field.toPlainText()
        )

        message = parse_response(response)

        db = dialog_box(message)
        db.exec()

        if message == SUCCESS_RESPONSE["publish"]:
            self.clear_form()
            self.load_excerpts()

        db.close()

    def clear_form(self):
        self.publish_tab.author_field.clear()
        self.publish_tab.work_field.clear()
        self.publish_tab.body_field.clear()

    def load_excerpts(self):
        try:
            self.table.clear()
        except AttributeError:
            pass

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
        super(EditWindow, self).__init__(parent)
        self.excerpt = excerpt
        self.setup_window()
        self.init_ui()
    
    def setup_window(self):
        self.setWindowTitle(str(self.excerpt))
        self.resize(800, 600)

    def init_ui(self):
        create_form_fields(self, self.excerpt)

        update_button = QPushButton(self)
        update_button.setText("Update")
        update_button.setGeometry(QRect(640, 465, 120, 40))
        update_button.clicked.connect(self.update_excerpt)

        delete_button = QPushButton(self)
        delete_button.setText("Delete")
        delete_button.setGeometry(510, 465, 120, 40)
        delete_button.clicked.connect(self.delete_excerpt)

    def update_excerpt(self):
        response = API.update_excerpt(
            self.excerpt.id,
            self.author_field.text(),
            self.work_field.text(),
            self.body_field.toPlainText()
        )

        self.handle_response(response, "update")

    def delete_excerpt(self):
        mb = QMessageBox()
        mb.setInformativeText("Are you sure you want to delete this excerpt?")
        mb.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        ret = mb.exec()

        if ret == QMessageBox.StandardButton.Yes:
            mb.close()
            response = API.delete_excerpt(self.excerpt.id)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainUI()
    main.show()
    sys.exit(app.exec())
