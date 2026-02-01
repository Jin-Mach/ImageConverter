from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QComboBox, QPushButton, \
    QDialogButtonBox, QWidget, QFileDialog

from src.Helpers.error_handler import ErrorHandler
from src.Helpers.language_provider import LanguageProvider
from src.Helpers.settings_provider import SettingsProvider
from src.Helpers.string_helper import validate_path

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


# noinspection PyTypeChecker
class SettingsDialog(QDialog):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.setObjectName("settingsDialog")
        self.setFixedSize(600, 400)
        self.main_window = main_window
        self.setLayout(self.create_gui())
        self.ui_texts = LanguageProvider().get_ui_texts(self.objectName())
        self.set_ui_texts()
        self.set_settings_data()

    def create_gui(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()
        path_group = QGroupBox()
        path_group.setObjectName("pathGroup")
        path_layout = QVBoxLayout()
        input_label = QLabel()
        input_label.setObjectName("inputLabel")
        self.input_edit = QLineEdit()
        self.input_edit.setObjectName("inputEdit")
        self.input_edit.setReadOnly(True)
        input_button_set = QPushButton()
        input_button_set.setObjectName("inputButtonSet")
        input_button_set.clicked.connect(lambda: self.set_path(path=self.input_path, mode="input"))
        input_button_reset = QPushButton()
        input_button_reset.setObjectName("inputButtonReset")
        input_button_reset.clicked.connect(lambda: self.reset_path(mode="input"))
        input_row = QHBoxLayout()
        output_label = QLabel()
        output_label.setObjectName("outputLabel")
        self.output_edit = QLineEdit()
        self.output_edit.setObjectName("outputEdit")
        self.output_edit.setReadOnly(True)
        output_button_set = QPushButton()
        output_button_set.setObjectName("outputButtonSet")
        output_button_set.clicked.connect(lambda: self.set_path(path=self.output_path, mode="output"))
        output_button_reset = QPushButton()
        output_button_reset.setObjectName("outputButtonReset")
        output_button_reset.clicked.connect(lambda: self.reset_path(mode="output"))
        output_row = QHBoxLayout()
        options_group = QGroupBox()
        options_group.setObjectName("optionsGroup")
        options_layout = QVBoxLayout()
        format_layout = QHBoxLayout()
        format_label = QLabel()
        format_label.setObjectName("formatLabel")
        self.format_combo = QComboBox()
        self.format_combo.setObjectName("formatCombo")
        format_button_reset = QPushButton()
        format_button_reset.setObjectName("formatButtonReset")
        format_button_reset.clicked.connect(lambda: self.reset_option("format"))
        resolution_layout = QHBoxLayout()
        resolution_label = QLabel()
        resolution_label.setObjectName("resolutionLabel")
        self.resolution_combo = QComboBox()
        self.resolution_combo.setObjectName("resolutionCombo")
        resolution_button_reset = QPushButton()
        resolution_button_reset.setObjectName("resolutionButtonReset")
        resolution_button_reset.clicked.connect(lambda: self.reset_option("resolution"))
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Close)
        save_button = button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setObjectName("saveButton")
        save_button.clicked.connect(self.save_settings)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        button_box.accepted.connect(self.accepted)
        button_box.rejected.connect(self.reject)
        input_row.addWidget(input_label)
        input_row.addWidget(self.input_edit, 1)
        input_row.addWidget(input_button_set)
        input_row.addWidget(input_button_reset)
        output_row.addWidget(output_label)
        output_row.addWidget(self.output_edit)
        output_row.addWidget(output_button_set)
        output_row.addWidget(output_button_reset)
        path_layout.addLayout(input_row)
        path_layout.addLayout(output_row)
        path_group.setLayout(path_layout)
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        format_layout.addWidget(format_button_reset)
        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(self.resolution_combo)
        resolution_layout.addStretch()
        resolution_layout.addWidget(resolution_button_reset)
        options_layout.addLayout(format_layout)
        options_layout.addLayout(resolution_layout)
        options_group.setLayout(options_layout)
        main_layout.addWidget(path_group)
        main_layout.addWidget(options_group)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_texts(self) -> None:
        try:
            default_text = "Unknown text"
            widgets = self.findChildren(QWidget)
            if not self.ui_texts or not widgets:
                raise ValueError(f"Texts: {self.ui_texts} or {widgets} not found.")
            self.setWindowTitle(self.ui_texts.get("titleText", default_text))
            for widget in widgets:
                text_key = f"{widget.objectName()}Text"
                if text_key in self.ui_texts.keys():
                    if isinstance(widget, QGroupBox):
                        widget.setTitle(self.ui_texts.get(text_key, default_text))
                    elif isinstance(widget, (QLabel, QPushButton)):
                        widget.setText(self.ui_texts.get(text_key, default_text))
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def set_settings_data(self) -> None:
        try:
            settings_data = SettingsProvider.load_settings_data()
            default_data = settings_data.get("default", {})
            user_data = settings_data.get("user", {})
            self.default_input_path = default_data.get("input_path", "")
            self.default_output_path = default_data.get("output_path", "")
            self.default_format_value = default_data.get("format_value", "")
            self.default_resolution_value = default_data.get("resolution_value", "")
            self.input_path = user_data.get("input_path", "")
            self.output_path = user_data.get("output_path", "")
            self.input_edit.setText(validate_path(self.input_path))
            self.input_edit.setToolTip(self.input_path)
            self.output_edit.setText(validate_path(self.output_path))
            self.output_edit.setToolTip(self.output_path)
            self.format_combo.addItems(default_data.get("format_list", []))
            self.format_combo.setCurrentText(user_data.get("format_value", "JPEG"))
            self.resolution_combo.addItems(default_data.get("resolution_list", []))
            self.resolution_combo.setCurrentText(user_data.get("resolution_value", "1920x1080"))
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def set_path(self, path: str, mode: str) -> None:
        try:
            new_path = QFileDialog.getExistingDirectory(parent=self,
                                                        caption=self.ui_texts.get("dialogTitleText", "Select folder"),
                                                        directory=path)
            if new_path:
                if mode == "input":
                    self.input_path = new_path
                    self.input_edit.setText(validate_path(self.input_path))
                    self.input_edit.setToolTip(self.input_path)
                elif mode == "output":
                    self.output_path = new_path
                    self.output_edit.setText(validate_path(self.output_path))
                    self.output_edit.setToolTip(self.output_path)
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def reset_path(self, mode: str) -> None:
        try:
            if mode == "input":
                self.input_path = self.default_input_path
                self.input_edit.setText(validate_path(self.input_path))
                self.input_edit.setToolTip(self.input_path)
            elif mode == "output":
                self.output_path = self.default_output_path
                self.output_edit.setText(validate_path(self.output_path))
                self.output_edit.setToolTip(self.output_path)
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def reset_option(self, mode: str) -> None:
        try:
            if mode == "format":
                self.format_combo.setCurrentText(self.default_format_value)
            elif mode == "resolution":
                self.resolution_combo.setCurrentText(self.default_resolution_value)
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def save_settings(self) -> None:
        try:
            if not SettingsProvider.save_user_settings(self.input_path, self.output_path,
                                                       self.format_combo.currentText(),
                                                       self.resolution_combo.currentText()):
                raise IOError("Save settings failed.")
            self.main_window.update_settings_data(self.input_path, self.output_path, self.format_combo.currentText(),
                                                  self.resolution_combo.currentText())
            self.accept()
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)