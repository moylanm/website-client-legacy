# -.- coding: utf-8 -.-
import sys

from main_ui import MainUI
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainUI()
    main.show()
    sys.exit(app.exec())
