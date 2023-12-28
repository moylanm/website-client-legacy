# -.- coding: utf-8 -.-
import sys, os

from net_handler import NetHandler
from dotenv import load_dotenv
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication, QGroupBox, QLabel, QLineEdit, QMainWindow, QPushButton, QTabWidget, QTextEdit, QWidget

class Main(QMainWindow):

    def __init__(self, username, password, parent=None):
        super().__init__(parent)

        net_handler = NetHandler(username, password)

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
        self.publish_view = PublishTabView(net_handler, self.publish_tab)

        # Edit tab
        self.edit_view = EditTabView(net_handler, self.edit_tab)

class PublishTabView:

    def __init__(self, net_handler, parent):
        self.net_handler = net_handler

        self.group_box = QGroupBox(parent)
        self.group_box.resize(800, 560)
        self.author_label = QLabel(self.group_box)
        self.author_label.setText(u"Author :")
        self.author_label.setGeometry(QRect(15, 10, 60, 30))
        self.work_label = QLabel(self.group_box)
        self.work_label.setText(u"Work :")
        self.work_label.setGeometry(QRect(25, 50, 50, 30))
        self.body_label = QLabel(self.group_box)
        self.body_label.setText(u"Body :")
        self.body_label.setGeometry(QRect(25, 88, 60, 30))
        self.author_field = QLineEdit(self.group_box)
        self.author_field.setGeometry(QRect(70, 10, 330, 30))
        self.work_field = QLineEdit(self.group_box)
        self.work_field.setGeometry(QRect(70, 50, 330, 30))
        self.body_field = QTextEdit(self.group_box)
        self.body_field.setGeometry(QRect(70, 90, 690, 370))
        self.publish_button = QPushButton(self.group_box)
        self.publish_button.setText(u"Publish")
        self.publish_button.setGeometry(QRect(640, 465, 120, 40))
        self.publish_button.clicked.connect(self.publish)
        self.clear_button = QPushButton(self.group_box)
        self.clear_button.setText(u"Clear")
        self.clear_button.setGeometry(QRect(510, 465, 120, 40))
        self.clear_button.clicked.connect(self.clear)
    
    def publish(self):
        print(self.author_field.text())
        print(self.work_field.text())
        print(self.body_field.toPlainText())

    def clear(self):
        self.author_field.setText("")
        self.work_field.setText("")
        self.body_field.setText("")

class EditTabView:

    def __init__(self, net_handler, parent):
        self.net_handler = net_handler

        self.group_box = QGroupBox(parent)
        self.group_box.resize(800, 560)
        for excerpt in self.net_handler.list_excerpts():
            print(excerpt)


if __name__ == "__main__":
    load_dotenv()

    app = QApplication(sys.argv)
    main = Main(os.getenv("USERNAME"), os.getenv("PASSWORD"))

    main.show()
    sys.exit(app.exec())
