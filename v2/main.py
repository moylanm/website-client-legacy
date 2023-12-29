# -.- coding: utf-8 -.-
import sys

from net_handler import RequestHandler
from PySide6.QtCore import QRect, Qt
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTextEdit,
    QWidget
)

REQUEST_HANDLER = RequestHandler()

class Main(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(u"Website Client")
        self.resize(800, 600)

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
        self.publish_view = PublishTabView(self.publish_tab)

        # Edit tab
        self.edit_view = EditTabView(self.edit_tab)

class PublishTabView:

    def __init__(self, parent):
        self.author_label = QLabel(parent)
        self.author_label.setText(u"Author :")
        self.author_label.setGeometry(QRect(15, 10, 60, 30))
        self.work_label = QLabel(parent)
        self.work_label.setText(u"Work :")
        self.work_label.setGeometry(QRect(25, 50, 50, 30))
        self.body_label = QLabel(parent)
        self.body_label.setText(u"Body :")
        self.body_label.setGeometry(QRect(25, 88, 60, 30))
        self.author_field = QLineEdit(parent)
        self.author_field.setGeometry(QRect(70, 10, 330, 30))
        self.work_field = QLineEdit(parent)
        self.work_field.setGeometry(QRect(70, 50, 330, 30))
        self.body_field = QTextEdit(parent)
        self.body_field.setGeometry(QRect(70, 90, 690, 370))
        self.publish_button = QPushButton(parent)
        self.publish_button.setText(u"Publish")
        self.publish_button.setGeometry(QRect(640, 465, 120, 40))
        self.publish_button.clicked.connect(self.publish)
        self.clear_button = QPushButton(parent)
        self.clear_button.setText(u"Clear")
        self.clear_button.setGeometry(QRect(510, 465, 120, 40))
        self.clear_button.clicked.connect(self.clear)
    
    def publish(self):
        res = REQUEST_HANDLER.publish_excerpt(
            self.author_field.text(),
            self.work_field.text(),
            self.body_field.toPlainText()
        )

        print(res)

    def clear(self):
        self.author_field.setText("")
        self.work_field.setText("")
        self.body_field.setText("")

class EditTabView:

    def __init__(self, parent):
        self.excerpts = REQUEST_HANDLER.list_excerpts()
        self.edit_window = None

        self.table = QTableWidget(len(self.excerpts), 1, parent)
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
    
    def on_clicked(self, excerpt):
        def new_window():
            self.edit_window = EditWindow(excerpt)
            self.edit_window.show()
        return new_window

class EditWindow(QMainWindow):

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
        self.publish_button = QPushButton(self)
        self.publish_button.setText(u"Update")
        self.publish_button.setGeometry(QRect(640, 465, 120, 40))
        self.publish_button.clicked.connect(self.update_excerpt)
        self.clear_button = QPushButton(self)
        self.clear_button.setText(u"Delete")
        self.clear_button.setGeometry(QRect(510, 465, 120, 40))
        self.clear_button.clicked.connect(self.delete_excerpt)

    def update_excerpt(self):
        res = REQUEST_HANDLER.update_excerpt(
            self.excerpt_id,
            self.author_field.text(),
            self.work_field.text(),
            self.body_field.toPlainText()
        )

        print(res)

    def delete_excerpt(self):
        # TODO: confirmation prompt

        res = REQUEST_HANDLER.delete_excerpt(self.excerpt_id)

        print(res)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()

    main.show()
    sys.exit(app.exec())
