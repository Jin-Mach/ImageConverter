from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QApplication


class DialogsProvider:
    class_name = "DialogsProvider"

    @staticmethod
    def get_error_dialog(error_message: str, parent=None) -> None:
        dialog = QDialog()
        dialog.setObjectName("errorDialog")
        if parent:
            dialog.setParent(parent)
        dialog.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Dialog)
        dialog.setModal(True)
        if QApplication.activeWindow():
            dialog.setWindowTitle(QApplication.activeWindow().windowTitle())
        main_layout = QVBoxLayout()
        error_label = QLabel()
        error_label.setText(error_message)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(dialog.reject)
        main_layout.addWidget(error_label)
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        dialog.exec()