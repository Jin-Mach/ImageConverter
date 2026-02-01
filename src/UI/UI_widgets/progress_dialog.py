from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QProgressBar, QHBoxLayout, QListWidget, QLabel, \
    QDialogButtonBox

from src.Helpers.string_helper import validate_path

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class ProgressDialog(QDialog):
    def __init__(self, parent: "MainWindow") -> None:
        super().__init__(parent)
        self.setObjectName("progressDialog")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setMinimumWidth(400)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel()
        self.paths_list_widget = QListWidget()
        self.paths_list_widget.hide()
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.button_box.hide()
        close_button = self.button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.clicked.connect(self.reject)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        main_layout.addLayout(progress_layout)
        main_layout.addWidget(self.paths_list_widget)
        main_layout.addWidget(self.button_box)
        return main_layout

    def update_progress(self, progress_data: list[int]) -> None:
        self.progress_label.setText(f"{progress_data[0]}/{progress_data[1]}")
        self.progress_bar.setValue(progress_data[0])
        self.progress_bar.setMaximum(progress_data[1])

    def progress_completed(self, paths_data: list[str]) -> None:
        self.progress_bar.setValue(self.progress_bar.maximum())
        if len(paths_data) > 0:
            for path in paths_data:
                self.paths_list_widget.addItem(validate_path(path))
            self.paths_list_widget.show()
            self.button_box.show()
            self.adjustSize()
        else:
            self.accept()