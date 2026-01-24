from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QComboBox, QCheckBox, QApplication, QSpinBox

from src.Helpers.error_handler import ErrorHandler
from src.Helpers.language_provider import LanguageProvider
from src.UI.UI_widgets.list_view import ListView


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainWindow")
        self.setCentralWidget(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QWidget:
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        self.title_label = QLabel()
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 20))
        self.images_group = QGroupBox()
        self.images_group.setObjectName("imagesGroup")
        images_layout = QHBoxLayout()
        self.image_path_text = QLabel()
        self.image_path_text.setObjectName("imagePathLabel")
        self.image_path_edit = QLineEdit()
        self.image_path_edit.setObjectName("imagePathEdit")
        self.image_path_edit.setReadOnly(True)
        self.image_button = QPushButton()
        self.image_button.setObjectName("imageButton")
        self.list_view = ListView()
        self.output_group = QGroupBox()
        self.output_group.setObjectName("outputGroup")
        output_layout = QHBoxLayout()
        self.output_path_label = QLabel()
        self.output_path_label.setObjectName("outputPathLabel")
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setObjectName("outputPathEdit")
        self.output_path_edit.setReadOnly(True)
        self.output_path_button = QPushButton()
        self.output_path_button.setObjectName("outputButton")
        self.options_group = QGroupBox()
        self.options_group.setObjectName("optionsGroup")
        options_layout = QVBoxLayout()
        self.format_group = QGroupBox()
        self.format_group.setObjectName("formatGroup")
        format_layout = QHBoxLayout()
        self.format_label = QLabel()
        self.format_label.setObjectName("formatLabel")
        self.format_combobox = QComboBox()
        self.format_combobox.setObjectName("formatComboBox")
        self.resize_group = QGroupBox()
        self.resize_group.setObjectName("resizeGroup")
        resize_layout = QVBoxLayout()
        size_layout = QHBoxLayout()
        self.width_label = QLabel()
        self.width_label.setObjectName("widthLabel")
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setObjectName("widthSpinbox")
        self.height_label = QLabel()
        self.height_label.setObjectName("heightLabel")
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setObjectName("heightSpinbox")
        ratio_layout = QHBoxLayout()
        self.ratio_label = QLabel()
        self.ratio_label.setObjectName("ratioLabel")
        self.ratio_checkbox = QCheckBox()
        self.ratio_checkbox.setObjectName("ratioCheckbox")
        convert_layout = QHBoxLayout()
        self.convert_button = QPushButton()
        self.convert_button.setObjectName("convertButton")
        images_layout.addWidget(self.image_path_text)
        images_layout.addWidget(self.image_path_edit)
        images_layout.addWidget(self.image_button)
        output_layout.addWidget(self.output_path_label)
        output_layout.addWidget(self.output_path_edit)
        output_layout.addWidget(self.output_path_button)
        format_layout.addWidget(self.format_label)
        format_layout.addWidget(self.format_combobox)
        size_layout.addWidget(self.width_label)
        size_layout.addWidget(self.width_spinbox)
        size_layout.addWidget(self.height_label)
        size_layout.addWidget(self.height_spinbox)
        ratio_layout.addWidget(self.ratio_label)
        ratio_layout.addWidget(self.ratio_checkbox)
        ratio_layout.addStretch()
        resize_layout.addLayout(size_layout)
        resize_layout.addLayout(ratio_layout)
        self.format_group.setLayout(format_layout)
        self.resize_group.setLayout(resize_layout)
        options_layout.addWidget(self.format_group)
        options_layout.addWidget(self.resize_group)
        convert_layout.addStretch()
        convert_layout.addWidget(self.convert_button)
        convert_layout.addStretch()
        self.images_group.setLayout(images_layout)
        self.output_group.setLayout(output_layout)
        self.options_group.setLayout(options_layout)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.images_group)
        main_layout.addWidget(self.list_view)
        main_layout.addWidget(self.output_group)
        main_layout.addWidget(self.options_group)
        main_layout.addLayout(convert_layout)
        central_widget.setLayout(main_layout)
        return central_widget

    def set_ui_text(self) -> None:
        try:
            default_text = "Unknown text"
            ui_texts = LanguageProvider.get_ui_texts(self.objectName())
            widgets = self.findChildren(QWidget)
            if not ui_texts or not widgets:
                raise ValueError(f"Texts: {ui_texts} or {widgets} not found.")
            self.setWindowTitle(ui_texts.get("titleText", ""))
            for widget in widgets:
                text_key = f"{widget.objectName()}Text"
                if text_key in ui_texts.keys():
                    if isinstance(widget, (QLabel, QPushButton)):
                        widget.setText(ui_texts.get(text_key, default_text))
                    elif isinstance(widget, QGroupBox):
                        widget.setTitle(ui_texts.get(text_key, default_text))
                    elif isinstance(widget, QLineEdit):
                        widget.setPlaceholderText(ui_texts.get(text_key, default_text))
        except Exception as e:
            ui_texts = LanguageProvider.get_ui_texts("errorDialog")
            ErrorHandler.exception_handler(self.__class__.__name__, e, ui_texts=ui_texts, parent=self)

    def showEvent(self, event: QEvent) -> None:
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        width = self.width() + 50
        height = self.height()
        self.setFixedSize(width, height)
        self.move((geometry.width() - width) // 2, (geometry.height() - height) // 2)