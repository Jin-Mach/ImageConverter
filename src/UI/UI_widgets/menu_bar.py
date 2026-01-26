from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QMenu

from src.Helpers.error_handler import ErrorHandler
from src.Helpers.language_provider import LanguageProvider
from src.UI.UI_widgets.about_dialog import AboutDialog
from src.UI.UI_widgets.settings_dialog import SettingsDialog


class MenuBar(QMenuBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("menuBar")
        self.parent = parent
        self.addMenu(self.create_ui())
        self.set_ui_texts()

    def create_ui(self) -> QMenu:
        main_menu = QMenu("", self)
        main_menu.setObjectName("mainMenu")
        setting_action = QAction("", main_menu)
        setting_action.setObjectName("settingsAction")
        setting_action.triggered.connect(self.show_settings_dialog)
        about_action = QAction("", main_menu)
        about_action.setObjectName("aboutAction")
        about_action.triggered.connect(self.show_about_dialog)
        main_menu.addAction(setting_action)
        main_menu.addSeparator()
        main_menu.addAction(about_action)
        return main_menu

    def set_ui_texts(self) -> None:
        try:
            default_text = "Unknown text"
            ui_texts = LanguageProvider.get_ui_texts(self.objectName())
            widgets = self.findChildren((QMenu, QAction))
            if not ui_texts or not widgets:
                raise ValueError(f"Texts: {ui_texts} or {widgets} not found.")
            for widget in widgets:
                text_key = f"{widget.objectName()}Text"
                if text_key in ui_texts.keys():
                    if isinstance(widget, QMenu):
                        widget.setTitle(ui_texts.get(text_key, default_text))
                    elif isinstance(widget, QAction):
                        widget.setText(ui_texts.get(text_key, default_text))
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self.parent)

    def show_about_dialog(self) -> None:
        try:
            dialog = AboutDialog(self)
            dialog.exec()
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self.parent)

    def show_settings_dialog(self) -> None:
        try:
            dialog = SettingsDialog(self)
            dialog.exec()
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self.parent)