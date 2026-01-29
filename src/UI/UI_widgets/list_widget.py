from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QPushButton

from src.Helpers.error_handler import ErrorHandler
from src.Helpers.string_helper import validate_path

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class ListWidget(QListWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.setObjectName("listWidget")
        self.main_window = main_window

    def set_items(self, images_paths: list[str]) -> None:
        try:
            self.clear()
            for image_path in images_paths:
                list_item = QListWidgetItem()
                item_widget = QWidget()
                item_layout = QHBoxLayout()
                path_label = QLabel()
                path_label.setText(validate_path(image_path, limit=40))
                path_button = QPushButton("delete")
                path_button.clicked.connect(lambda _, current_item=list_item: self.delete_current_item(current_item))
                item_layout.addWidget(path_label)
                item_layout.addStretch()
                item_layout.addWidget(path_button)
                item_widget.setLayout(item_layout)
                self.addItem(list_item)
                self.setItemWidget(list_item, item_widget)
                list_item.setSizeHint(item_widget.sizeHint())
                list_item.setStatusTip(image_path)
        except Exception as e:
            ErrorHandler.exception_handler(self.__class__.__name__, e, parent=self.main_window)

    def delete_current_item(self, item: QListWidgetItem) -> None:
        row = self.row(item)
        if row >= 0:
            self.takeItem(row)