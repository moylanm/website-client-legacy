# -.- coding: utf-8 -.-
import math

from excerpt import Excerpt
from excerpt_manager import ExcerptManager
from helpers import create_form_fields, dialog_box
from PySide6.QtCore import Signal, QRect
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox


class EditWindow(QMainWindow):

    edit_event = Signal()

    def __init__(self, excerpt: Excerpt, excerpt_manager: ExcerptManager, parent=None):
        super(EditWindow, self).__init__(parent)
        self.excerpt = excerpt
        self.excerpt_manager = excerpt_manager
        self.setup_window()
        self.init_ui()
    
    def setup_window(self):
        self.setWindowTitle(str(self.excerpt))
        self.resize(800, 600)
        self.move_window()

    def move_window(self):
        screen = QApplication.primaryScreen().geometry()

        x = math.floor((screen.width() - self.width()) // 1.5)
        y = math.floor((screen.height() - self.height()) // 1.5)
        
        self.move(x, y)

    def init_ui(self):
        create_form_fields(self, self.excerpt)
        self.create_button("Update", QRect(640, 465, 120, 40), self.update_excerpt)
        self.create_button("Delete", QRect(510, 465, 120, 40), self.confirm_delete)

    def create_button(self, text, geometry, callback):
        button = QPushButton(text, self)
        button.setGeometry(geometry)
        button.clicked.connect(callback)

    def update_excerpt(self):
        author = self.author_field.text()
        work = self.work_field.text()
        body = self.body_field.toPlainText()

        response = self.excerpt_manager.update_excerpt(self.excerpt.id, author, work, body)
        self.handle_response(response)

    def delete_excerpt(self):
        response = self.excerpt_manager.delete_excerpt(self.excerpt.id)
        self.handle_response(response)

    def confirm_delete(self):
        mb = QMessageBox()
        mb.setInformativeText("Are you sure you want to delete this excerpt?")
        mb.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if mb.exec() == QMessageBox.StandardButton.Yes:
            self.delete_excerpt()

    def handle_response(self, response):
        db = dialog_box(response["message"])
        db.exec()

        if response["success"]:
            self.edit_event.emit()
            self.close()

        db.close()
