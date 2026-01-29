from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QComboBox, QCheckBox, QApplication, QFileDialog

from src.Helpers.error_handler import ErrorHandler
from src.Helpers.language_provider import LanguageProvider
from src.Helpers.settings_provider import SettingsProvider
from src.Helpers.string_helper import validate_path
from src.UI.UI_widgets.list_view import ListView
from src.UI.UI_widgets.menu_bar import MenuBar


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainWindow")
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)
        self.set_basic_data()
        self.setCentralWidget(self.create_gui())
        self.set_ui_text()
        self.set_settings_data()

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
        self.image_button.clicked.connect(self.set_images_path)
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
        self.output_path_button.clicked.connect(self.set_output_path)
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
        self.size_group = QGroupBox()
        self.size_group.setObjectName("sizeGroup")
        size_layout = QVBoxLayout()
        resolution_layout = QHBoxLayout()
        self.resolution_label = QLabel()
        self.resolution_label.setObjectName("resolutionLabel")
        self.resolution_combobox = QComboBox()
        self.resolution_combobox.setObjectName("resolutionComboBox")
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
        format_layout.addStretch()
        resolution_layout.addWidget(self.resolution_label)
        resolution_layout.addWidget(self.resolution_combobox)
        resolution_layout.addStretch()
        ratio_layout.addWidget(self.ratio_label)
        ratio_layout.addWidget(self.ratio_checkbox)
        ratio_layout.addStretch()
        size_layout.addLayout(resolution_layout)
        size_layout.addLayout(ratio_layout)
        self.format_group.setLayout(format_layout)
        self.size_group.setLayout(size_layout)
        options_layout.addWidget(self.format_group)
        options_layout.addWidget(self.size_group)
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

    def set_basic_data(self) -> None:
        try:
            self.ui_texts = LanguageProvider.get_ui_texts(self.objectName())
            self.settings_data = SettingsProvider.load_settings_data()
            self.default_data = self.settings_data.get("default", {})
            self.user_data = self.settings_data.get("user", {})
            self.usage_path = self.user_data.get("output_path", "")
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def set_ui_text(self) -> None:
        try:
            default_text = "Unknown text"
            widgets = self.findChildren(QWidget)
            if not self.ui_texts or not widgets:
                raise ValueError(f"Texts: {self.ui_texts} or {widgets} not found.")
            self.setWindowTitle(self.ui_texts.get("titleText", ""))
            for widget in widgets:
                text_key = f"{widget.objectName()}Text"
                if text_key in self.ui_texts.keys():
                    if isinstance(widget, (QLabel, QPushButton)):
                        widget.setText(self.ui_texts.get(text_key, default_text))
                    elif isinstance(widget, QGroupBox):
                        widget.setTitle(self.ui_texts.get(text_key, default_text))
                    elif isinstance(widget, QLineEdit):
                        widget.setPlaceholderText(self.ui_texts.get(text_key, default_text))
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def set_settings_data(self) -> None:
        try:
            self.image_path_edit.setText(validate_path(self.user_data.get("input_path", "")))
            self.image_path_edit.setToolTip(self.user_data.get("input_path", ""))
            self.output_path_edit.setText(validate_path(self.user_data.get("output_path", "")))
            self.output_path_edit.setToolTip(self.user_data.get("output_path", ""))
            self.format_combobox.addItems(self.default_data.get("format_list", []))
            self.format_combobox.setCurrentText(self.user_data.get("format_value", "JPEG"))
            self.resolution_combobox.addItems(self.default_data.get("resolution_list", []))
            self.resolution_combobox.setCurrentText(self.user_data.get("resolution_value", "1920x1080"))
            self.ratio_checkbox.setChecked(self.user_data.get("ratio_checkbox", True))
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def update_settings_data(self, input_path: str, output_path: str, format_value: str, resolution_value: str) -> None:
        try:
            self.image_path_edit.setText(validate_path(input_path))
            self.image_path_edit.setToolTip(input_path)
            self.output_path_edit.setText(validate_path(output_path))
            self.output_path_edit.setToolTip(output_path)
            self.format_combobox.setCurrentText(format_value)
            self.resolution_combobox.setCurrentText(resolution_value)
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def set_images_path(self) -> None:
        try:
            files = ""
            if self.default_data:
                for files_format in self.default_data.get("format_list", []):
                    if files_format:
                        files += f"*.{files_format.lower()} "
            files_filter = f"{self.ui_texts.get('imageFilterText', 'Select images')} ({files.strip()})"
            paths, _ = QFileDialog.getOpenFileNames(parent=self,
                                                    caption=self.ui_texts.get("imagesTitleText", "Select images"),
                                                    directory=self.user_data.get("input_path", ""),
                                                    filter=files_filter)
            if paths:
                print(f"paths:{paths}")
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def set_output_path(self) -> None:
        try:
            path = QFileDialog.getExistingDirectory(parent=self,
                                                    caption=self.ui_texts.get("outputTitleText", "Select path"),
                                                    directory=self.usage_path)
            if path:
                self.usage_path = path
                self.output_path_edit.setText(validate_path(path))
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def showEvent(self, event: QEvent) -> None:
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        width = self.width() + 50
        height = self.height()
        self.setFixedSize(width, height)
        self.move((geometry.width() - width) // 2, (geometry.height() - height) // 2)