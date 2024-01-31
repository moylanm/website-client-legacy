from PySide6.QtCore import Qt, QRect
from edit_window import EditWindow
from excerpt_manager import ExcerptManager
from helpers import create_form_fields, dialog_box
from PySide6.QtWidgets import QHeaderView, QMainWindow, QPushButton, QTabWidget, QTableWidget, QWidget

class MainUI(QMainWindow):

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.excerpts = []
        self.excerpt_manager = ExcerptManager()
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
        author = self.publish_tab.author_field.text()
        work = self.publish_tab.work_field.text()
        body = self.publish_tab.body_field.toPlainText()

        response = self.excerpt_manager.publish_excerpt(author, work, body)

        db = dialog_box(response["message"])
        db.exec()

        if response["success"]:
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

        self.excerpts = self.excerpt_manager.list_excerpts()
        
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
            self.edit_window = EditWindow(excerpt, self.excerpt_manager, parent=self)
            self.edit_window.edit_event.connect(self.load_excerpts)
            self.edit_window.show()

        return new_edit_window
