from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QComboBox, QCheckBox, QApplication, QFileDialog, QSizePolicy, QMessageBox

from src.Helpers.error_handler import ErrorHandler
from src.Helpers.language_provider import LanguageProvider
from src.Helpers.settings_provider import SettingsProvider
from src.Helpers.string_helper import validate_path
from src.Helpers.threading_provider import ThreadingProvider
from src.UI.UI_widgets.list_widget import ListWidget
from src.UI.UI_widgets.menu_bar import MenuBar
from src.UI.UI_widgets.progress_dialog import ProgressDialog


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
        self.images_group = QGroupBox()
        self.images_group.setObjectName("imagesGroup")
        images_layout = QHBoxLayout()
        self.image_path_text = QLabel()
        self.image_path_text.setObjectName("imagePathLabel")
        self.image_path_edit = QLineEdit()
        self.image_path_edit.setObjectName("imagePathEdit")
        self.image_path_edit.setReadOnly(True)
        self.replace_images_button = QPushButton()
        self.replace_images_button.setObjectName("replaceImagesButton")
        self.replace_images_button.clicked.connect(lambda: self.set_images_path(clear=True))
        self.add_images_button = QPushButton()
        self.add_images_button.setObjectName("addImagesButton")
        self.add_images_button.clicked.connect(lambda: self.set_images_path(clear=False))
        self.list_widget = ListWidget(self)
        self.list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.list_widget.model().rowsRemoved.connect(self.update_images_count_label)
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
        delete_layout = QHBoxLayout()
        self.images_count_label = QLabel()
        self.images_count_label.setObjectName("imagesCountLabel")
        self.clear_list_button = QPushButton()
        self.clear_list_button.setObjectName("clearListButton")
        self.clear_list_button.clicked.connect(self.clear_list)
        self.options_group = QGroupBox()
        self.options_group.setObjectName("optionsGroup")
        options_layout = QHBoxLayout()
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
        self.convert_button.clicked.connect(self.start_convert)
        images_layout.addWidget(self.image_path_text)
        images_layout.addWidget(self.image_path_edit)
        images_layout.addWidget(self.replace_images_button)
        images_layout.addWidget(self.add_images_button)
        output_layout.addWidget(self.output_path_label)
        output_layout.addWidget(self.output_path_edit)
        output_layout.addWidget(self.output_path_button)
        delete_layout.addWidget(self.images_count_label)
        delete_layout.addStretch()
        delete_layout.addWidget(self.clear_list_button)
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
        main_layout.addWidget(self.images_group)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(delete_layout)
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
            self.full_output_path = self.user_data.get("output_path", "")
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
                        if widget.objectName() == "imagesCountLabel":
                            self.images_count_label.setText(
                                f"{self.ui_texts.get("imagesCountLabelText", "Files count:")} 0")
                        else:
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

    def set_images_path(self, clear: bool) -> None:
        try:
            files = ""
            if self.default_data:
                for files_format in self.default_data.get("format_list", []):
                    if files_format:
                        files += f"*.{files_format.lower()} "
            files_filter = f"{self.ui_texts.get('imageFilterText', 'Select images')} ({files.strip()})"
            self.selected_paths, _ = QFileDialog.getOpenFileNames(parent=self,
                                                    caption=self.ui_texts.get("imagesTitleText", "Select images"),
                                                    directory=self.user_data.get("input_path", ""),
                                                    filter=files_filter)
            if self.selected_paths:
                self.list_widget.set_items(self.selected_paths, clear)
            self.update_images_count_label()
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def set_output_path(self) -> None:
        try:
            path = QFileDialog.getExistingDirectory(parent=self,
                                                    caption=self.ui_texts.get("outputTitleText", "Select folder"),
                                                    directory=self.full_output_path)
            if path:
                self.full_output_path = path
                self.output_path_edit.setText(validate_path(path))
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def start_convert(self) -> None:
        try:
            paths_list = self.list_widget.get_all_paths()
            if paths_list:
                progress_dialog = ProgressDialog(self)
                progress_dialog.show()
                self.threading_provider = ThreadingProvider(paths_list, self.full_output_path,
                                                            self.format_combobox.currentText(),
                                                            self.resolution_combobox.currentText(),
                                                            self.ratio_checkbox.isChecked())
                self.threading_provider.convert_object.convert_progress.connect(progress_dialog.update_progress)
                self.threading_provider.convert_object.convert_failed_list.connect(progress_dialog.progress_completed)
                self.threading_provider.start_conversion()
                self.threading_provider.convert_thread.start()
            else:
                QMessageBox.information(self, self.ui_texts.get("titleText", ""),
                                        self.ui_texts.get("noPathsText", "No images selected for conversion"))
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self)

    def update_images_count_label(self) -> None:
        self.images_count_label.setText(f"{self.ui_texts.get("imagesCountLabelText", "Files count:")} {self.list_widget.count()}")

    def clear_list(self) -> None:
        self.list_widget.clear()
        self.update_images_count_label()

    def showEvent(self, event: QEvent) -> None:
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        self.setMinimumSize(600, 700)
        width = self.width()
        height = self.height()
        self.move((geometry.width() - width) // 2, (geometry.height() - height) // 2)