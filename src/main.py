import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from src.UI.main_window import MainWindow


def create_app() -> None:
    application = QApplication(sys.argv)
    if sys.platform == "darwin":
        application.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, True)
    main_window = MainWindow()
    main_window.show()
    sys.exit(application.exec())