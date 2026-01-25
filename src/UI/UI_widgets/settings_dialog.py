from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QSpinBox, QComboBox, \
    QPushButton, QDialogButtonBox, QWidget

from src.Helpers.error_handler import ErrorHandler
from src.Helpers.language_provider import LanguageProvider


# noinspection PyTypeChecker
class SettingsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("settingsDialog")
        self.setFixedSize(600, 400)
        self.parent = parent
        self.setLayout(self.create_gui())
        self.set_ui_texts()

    def create_gui(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()
        path_group = QGroupBox()
        path_group.setObjectName("pathGroup")
        path_layout = QVBoxLayout()
        input_label = QLabel()
        input_label.setObjectName("inputLabel")
        input_edit = QLineEdit()
        input_edit.setObjectName("inputEdit")
        input_edit.setReadOnly(True)
        input_button_set = QPushButton()
        input_button_set.setObjectName("inputButtonSet")
        input_button_reset = QPushButton()
        input_button_reset.setObjectName("inputButtonReset")
        input_row = QHBoxLayout()
        output_label = QLabel()
        output_label.setObjectName("outputLabel")
        output_edit = QLineEdit()
        output_edit.setObjectName("outputEdit")
        output_edit.setReadOnly(True)
        output_button_set = QPushButton()
        output_button_set.setObjectName("outputButtonSet")
        output_button_reset = QPushButton()
        output_button_reset.setObjectName("outputButtonReset")
        output_row = QHBoxLayout()
        options_group = QGroupBox()
        options_group.setObjectName("optionsGroup")
        options_layout = QVBoxLayout()
        format_label = QLabel()
        format_label.setObjectName("formatLabel")
        format_combo = QComboBox()
        format_combo.setObjectName("formatCombo")
        format_combo.addItems(["PNG", "JPEG", "BMP"])
        format_button_set = QPushButton()
        format_button_set.setObjectName("formatButtonSet")
        format_button_reset = QPushButton()
        format_button_reset.setObjectName("formatButtonReset")
        format_layout = QHBoxLayout()
        size_label_width = QLabel()
        size_label_width.setObjectName("widthLabel")
        width_spin = QSpinBox()
        width_spin.setObjectName("widthSpin")
        width_spin.setRange(1, 10000)
        size_label_height = QLabel()
        size_label_height.setObjectName("heightLabel")
        size_label_height.setContentsMargins(20, 0, 0, 0)
        height_spin = QSpinBox()
        height_spin.setObjectName("heightSpin")
        height_spin.setRange(1, 10000)
        size_button_set = QPushButton()
        size_button_set.setObjectName("sizeButtonSet")
        size_button_reset = QPushButton()
        size_button_reset.setObjectName("sizeButtonReset")
        size_layout = QHBoxLayout()
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Close)
        save_button = button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setObjectName("saveButton")
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        button_box.accepted.connect(self.accepted)
        button_box.rejected.connect(self.reject)
        input_row.addWidget(input_label)
        input_row.addWidget(input_edit, 1)
        input_row.addWidget(input_button_set)
        input_row.addWidget(input_button_reset)
        output_row.addWidget(output_label)
        output_row.addWidget(output_edit)
        output_row.addWidget(output_button_set)
        output_row.addWidget(output_button_reset)
        path_layout.addLayout(input_row)
        path_layout.addLayout(output_row)
        path_group.setLayout(path_layout)
        format_layout.addWidget(format_label)
        format_layout.addWidget(format_combo)
        format_layout.addStretch()
        format_layout.addWidget(format_button_set)
        format_layout.addWidget(format_button_reset)
        size_layout.addWidget(size_label_width)
        size_layout.addWidget(width_spin)
        size_layout.addWidget(size_label_height)
        size_layout.addWidget(height_spin)
        size_layout.addStretch()
        size_layout.addWidget(size_button_set)
        size_layout.addWidget(size_button_reset)
        options_layout.addLayout(format_layout)
        options_layout.addLayout(size_layout)
        options_group.setLayout(options_layout)
        main_layout.addWidget(path_group)
        main_layout.addWidget(options_group)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_texts(self) -> None:
        try:
            default_text = "Unknown text"
            ui_texts = LanguageProvider.get_ui_texts(self.objectName())
            widgets = self.findChildren(QWidget)
            if not ui_texts or not widgets:
                raise ValueError(f"Texts: {ui_texts} or {widgets} not found.")
            self.setWindowTitle(ui_texts.get("titleText", default_text))
            for widget in widgets:
                text_key = f"{widget.objectName()}Text"
                if text_key in ui_texts.keys():
                    if isinstance(widget, QGroupBox):
                        widget.setTitle(ui_texts.get(text_key, default_text))
                    elif isinstance(widget, (QLabel, QPushButton)):
                        widget.setText(ui_texts.get(text_key, default_text))
        except Exception as e:
            error_texts = LanguageProvider.get_ui_texts("errorDialog")
            ErrorHandler.exception_handler(self.__class__.__name__, e, ui_texts=error_texts, parent=self.parent)