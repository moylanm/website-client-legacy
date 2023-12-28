# -.- coding: utf-8 -.-
import sys

from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication, QGroupBox, QLabel, QLineEdit, QMainWindow, QPushButton, QTabWidget, QTextEdit, QWidget

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(u"Website Client")
        self.resize(800, 600)

        # Tabs
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QRect(0, 0, 800, 590))
        self.publishTab = QWidget()
        self.editTab = QWidget()
        self.tabWidget.addTab(self.publishTab, "")
        self.tabWidget.setTabText(0, u"Publish")
        self.tabWidget.addTab(self.editTab, "")
        self.tabWidget.setTabText(1, u"Edit")
        self.tabWidget.setCurrentIndex(0)

        # Publish tab
        self.publishGroupBox = QGroupBox(self.publishTab)
        self.publishGroupBox.resize(800, 560)
        self.authorLabel = QLabel(self.publishGroupBox)
        self.authorLabel.setText(u"Author :")
        self.authorLabel.setGeometry(QRect(15, 10, 60, 30))
        self.workLabel = QLabel(self.publishGroupBox)
        self.workLabel.setText(u"Work :")
        self.workLabel.setGeometry(QRect(25, 50, 50, 30))
        self.bodyLabel = QLabel(self.publishGroupBox)
        self.bodyLabel.setText(u"Body :")
        self.bodyLabel.setGeometry(QRect(25, 88, 60, 30))
        self.authorField = QLineEdit(self.publishGroupBox)
        self.authorField.setGeometry(QRect(70, 10, 330, 30))
        self.workField = QLineEdit(self.publishGroupBox)
        self.workField.setGeometry(QRect(70, 50, 330, 30))
        self.bodyField = QTextEdit(self.publishGroupBox)
        self.bodyField.setGeometry(QRect(70, 90, 690, 370))
        self.publishButton = QPushButton(self.publishGroupBox)
        self.publishButton.setText(u"Publish")
        self.publishButton.setGeometry(QRect(640, 465, 120, 40))
        self.publishButton.clicked.connect(self.publish)
        self.clearButton = QPushButton(self.publishGroupBox)
        self.clearButton.setText(u"Clear")
        self.clearButton.setGeometry(QRect(510, 465, 120, 40))
        self.clearButton.clicked.connect(self.clear)

    def publish(self):
        print(self.authorField.text())
        print(self.workField.text())
        print(self.bodyField.toPlainText())

    def clear(self):
        self.authorField.setText("")
        self.workField.setText("")
        self.bodyField.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
