from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QTextEdit, QDialogButtonBox, QPushButton, QWidget

from src.Helpers.error_handler import ErrorHandler
from src.Helpers.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class ManualDialog(QDialog):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.setObjectName("manualDialog")
        self.setFixedSize(600, 700)
        self.setLayout(self.create_gui())
        self.set_ui_texts()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.reject)
        main_layout.addWidget(text_edit)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_texts(self) -> None:
        try:
            ui_texts = LanguageProvider().get_ui_texts(self.objectName())
            text_edit_text = LanguageProvider.get_manual_text()
            default_text = "Unknown text"
            widgets = self.findChildren(QWidget)
            if not ui_texts or not text_edit_text or not widgets:
                raise ValueError(f"Texts: {ui_texts} or {text_edit_text} or {widgets} not found.")
            self.setWindowTitle(ui_texts.get("titleText", default_text))
            for widget in widgets:
                text_key = f"{widget.objectName()}Text"
                if text_key in ui_texts.keys():
                    if isinstance(widget, QPushButton):
                        widget.setText(ui_texts.get(text_key, default_text))
                if isinstance(widget, QTextEdit):
                    widget.setText(text_edit_text)
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e)