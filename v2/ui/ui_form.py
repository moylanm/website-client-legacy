# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QTabWidget,
    QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(818, 608)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 801, 591))
        self.publish = QWidget()
        self.publish.setObjectName(u"publish")
        self.groupBox = QGroupBox(self.publish)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(-1, -1, 801, 561))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(15, 10, 61, 31))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(25, 50, 51, 31))
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(25, 85, 61, 31))
        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(70, 10, 331, 31))
        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(70, 50, 331, 31))
        self.textEdit = QTextEdit(self.groupBox)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(70, 90, 691, 361))
        self.publish_button = QPushButton(self.groupBox)
        self.publish_button.setObjectName(u"publish_button")
        self.publish_button.setGeometry(QRect(640, 460, 121, 41))
        self.clear_button = QPushButton(self.groupBox)
        self.clear_button.setObjectName(u"clear_button")
        self.clear_button.setGeometry(QRect(510, 460, 121, 41))
        self.tabWidget.addTab(self.publish, "")
        self.edit = QWidget()
        self.edit.setObjectName(u"edit")
        self.tabWidget.addTab(self.edit, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Website Client", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Author :", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Work :", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Body :", None))
        self.publish_button.setText(QCoreApplication.translate("MainWindow", u"Publish", None))
        self.clear_button.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.publish), QCoreApplication.translate("MainWindow", u"Publish", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.edit), QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

