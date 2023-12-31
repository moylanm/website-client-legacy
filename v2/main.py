# -.- coding: utf-8 -.-
import sys

from request_handler import RequestHandler
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

REQUEST_HANDLER = RequestHandler()

SUCCESS_RESPONSE = {
    "publish": "excerpt successfully created",
    "update": "excerpt successfully updated",
    "delete": "excerpt successfully deleted"
}

class Main(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(u"Website Client")
        self.resize(800, 600)

        self.excerpts = []
        self.edit_window = None

        # Tabs
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(QRect(0, 0, 800, 590))
        self.publish_tab = QWidget()
        self.edit_tab = QWidget()
        self.tab_widget.addTab(self.publish_tab, "")
        self.tab_widget.setTabText(0, u"Publish")
        self.tab_widget.addTab(self.edit_tab, "")
        self.tab_widget.setTabText(1, u"Edit")
        self.tab_widget.setCurrentIndex(0)

        # Publish tab 
        self.author_label = QLabel(self.publish_tab)
        self.author_label.setText(u"Author :")
        self.author_label.setGeometry(QRect(15, 10, 60, 30))
        self.work_label = QLabel(self.publish_tab)
        self.work_label.setText(u"Work :")
        self.work_label.setGeometry(QRect(25, 50, 50, 30))
        self.body_label = QLabel(self.publish_tab)
        self.body_label.setText(u"Body :")
        self.body_label.setGeometry(QRect(25, 88, 60, 30))
        self.author_field = QLineEdit(self.publish_tab)
        self.author_field.setGeometry(QRect(70, 10, 330, 30))
        self.work_field = QLineEdit(self.publish_tab)
        self.work_field.setGeometry(QRect(70, 50, 330, 30))
        self.body_field = QTextEdit(self.publish_tab)
        self.body_field.setGeometry(QRect(70, 90, 690, 370))
        self.publish_button = QPushButton(self.publish_tab)
        self.publish_button.setText(u"Publish")
        self.publish_button.setGeometry(QRect(640, 465, 120, 40))
        self.publish_button.clicked.connect(self.publish)
        self.clear_button = QPushButton(self.publish_tab)
        self.clear_button.setText(u"Clear")
        self.clear_button.setGeometry(QRect(510, 465, 120, 40))
        self.clear_button.clicked.connect(self.clear)

        # Edit tab
        self.load_excerpts()

    def publish(self):
        response = REQUEST_HANDLER.publish_excerpt(
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
        self.author_field.setText("")
        self.work_field.setText("")
        self.body_field.setText("")

    def load_excerpts(self):
        self.excerpts = REQUEST_HANDLER.list_excerpts()

        self.table = QTableWidget(len(self.excerpts), 1, self.edit_tab)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.resize(800, 560)

        for row, excerpt in enumerate(self.excerpts):
            button = QPushButton(f"{excerpt}")
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
        
        self.setWindowTitle(f"{excerpt}")
        self.resize(800, 600)
        
        self.author_label = QLabel(self)
        self.author_label.setText(u"Author :")
        self.author_label.setGeometry(QRect(15, 10, 60, 30))
        self.work_label = QLabel(self)
        self.work_label.setText(u"Work :")
        self.work_label.setGeometry(QRect(25, 50, 50, 30))
        self.body_label = QLabel(self)
        self.body_label.setText(u"Body :")
        self.body_label.setGeometry(QRect(25, 88, 60, 30))
        self.author_field = QLineEdit(self)
        self.author_field.setGeometry(QRect(70, 10, 330, 30))
        self.author_field.setText(f"{excerpt.author}")
        self.work_field = QLineEdit(self)
        self.work_field.setGeometry(QRect(70, 50, 330, 30))
        self.work_field.setText(f"{excerpt.work}")
        self.body_field = QTextEdit(self)
        self.body_field.setGeometry(QRect(70, 90, 690, 370))
        self.body_field.setText(f"{excerpt.body}")
        self.update_button = QPushButton(self)
        self.update_button.setText(u"Update")
        self.update_button.setGeometry(QRect(640, 465, 120, 40))
        self.update_button.clicked.connect(self.update_excerpt)
        self.delete_button = QPushButton(self)
        self.delete_button.setText(u"Delete")
        self.delete_button.setGeometry(QRect(510, 465, 120, 40))
        self.delete_button.clicked.connect(self.delete_excerpt)

    def update_excerpt(self):
        response = REQUEST_HANDLER.update_excerpt(
            self.excerpt_id,
            self.author_field.text(),
            self.work_field.text(),
            self.body_field.toPlainText()
        )

        message = parse_response(response)

        db = dialog_box(message)
        db.exec()

        if message == SUCCESS_RESPONSE["update"]:
            self.edit_event.emit()
            self.close()

        db.close()

    def delete_excerpt(self):
        mb = QMessageBox()
        mb.setInformativeText("Are you sure you want to delete this excerpt?")
        mb.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        ret = mb.exec()

        if ret == QMessageBox.StandardButton.Yes:
            mb.close()

            response = REQUEST_HANDLER.delete_excerpt(self.excerpt_id)
            
            message = parse_response(response)

            db = dialog_box(message)
            db.exec()
            
            if message == SUCCESS_RESPONSE["delete"]:
                self.edit_event.emit()
                self.close()

            db.close()
        else:
            mb.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()

    main.show()
    sys.exit(app.exec())
