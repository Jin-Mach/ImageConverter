from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QPushButton

from src.Helpers.error_handler import ErrorHandler
from src.Helpers.language_provider import LanguageProvider
from src.Helpers.string_helper import validate_path

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class ListWidget(QListWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.setObjectName("listWidget")
        self.main_window = main_window
        self.ui_texts = LanguageProvider.get_ui_texts(self.objectName())

    def set_items(self, images_paths: list[str], clear: bool) -> None:
        try:
            if clear:
                self.clear()
            for image_path in images_paths:
                list_item = QListWidgetItem()
                list_item.setData(Qt.ItemDataRole.UserRole, image_path)
                item_widget = QWidget()
                item_layout = QHBoxLayout()
                path_label = QLabel()
                path_label.setText(validate_path(image_path, limit=50))
                path_button = QPushButton(self.ui_texts.get("pathButtonText", "Delete"))
                path_button.clicked.connect(lambda _, current_item=list_item: self.delete_current_item(current_item))
                item_layout.addWidget(path_label)
                item_layout.addStretch()
                item_layout.addWidget(path_button)
                item_widget.setLayout(item_layout)
                list_item.setSizeHint(item_widget.sizeHint())
                list_item.setStatusTip(image_path)
                self.addItem(list_item)
                self.setItemWidget(list_item, item_widget)
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self.main_window)

    def delete_current_item(self, item: QListWidgetItem) -> None:
        row = self.row(item)
        if row >= 0:
            self.takeItem(row)

    def get_all_paths(self) -> list[str]:
        paths_list = []
        try:
            for i in range(self.count()):
                item = self.item(i)
                ful_path = item.data(Qt.ItemDataRole.UserRole)
                paths_list.append(ful_path)
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self.main_window)
        return paths_list