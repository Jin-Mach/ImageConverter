from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QApplication


class DialogsProvider:

    @staticmethod
    def get_error_dialog(error_message: str, ui_texts=None, parent=None) -> None:
        dialog = QDialog()
        dialog.setObjectName("errorDialog")
        if parent:
            dialog.setParent(parent)
        dialog.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Dialog)
        dialog.setModal(True)
        if QApplication.activeWindow():
            dialog.setWindowTitle(QApplication.activeWindow().windowTitle())
        main_layout = QVBoxLayout()
        text_label = QLabel()
        text_label.setObjectName("textLabel")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label = QLabel()
        error_label.setText(error_message)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        button_box.rejected.connect(dialog.reject)
        main_layout.addWidget(text_label)
        main_layout.addWidget(error_label)
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        if ui_texts:
            text_label.setText(ui_texts.get(f"{text_label.objectName()}Text", "Unknown text"))
            close_button.setText(ui_texts.get(f"{close_button.objectName()}Text", "Unknown text"))
        dialog.exec()