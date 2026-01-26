import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from src.Helpers.error_handler import ErrorHandler
from src.Helpers.language_provider import LanguageProvider
from src.Helpers.settings_provider import SettingsProvider


class AppInit:

    @staticmethod
    def app_initialization(application: QApplication) -> bool:
        try:
            if sys.platform == "darwin":
                application.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, True)
            if not SettingsProvider.initialize_settings():
                return False
            ErrorHandler.ui_texts = LanguageProvider.get_ui_texts("errorDialog")
            return True
        except Exception as e:
            ErrorHandler.exception_handler(AppInit.__name__, e)
            return False