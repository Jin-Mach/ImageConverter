import sys

from PyQt6.QtWidgets import QApplication

from src.Helpers.app_init import AppInit
from src.Helpers.error_handler import ErrorHandler
from src.Helpers.language_provider import LanguageProvider
from src.UI.main_window import MainWindow


def create_app() -> None:
    try:
        application = QApplication(sys.argv)
        if not AppInit.app_initialization(application):
            raise RuntimeError("Application initialization failed")
        main_window = MainWindow()
        main_window.show()
        sys.exit(application.exec())
    except Exception as e:
        ErrorHandler.ui_texts = LanguageProvider.get_ui_texts("errorDialog")
        ErrorHandler.exception_handler(class_name="create_app method", exception=e)