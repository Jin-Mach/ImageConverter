from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QTextEdit, QDialogButtonBox, \
    QPushButton, QWidget

from src.Helpers.error_handler import ErrorHandler
from src.Helpers.language_provider import LanguageProvider


class AboutDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("aboutDialog")
        self.setFixedSize(500, 400)
        self.parent = parent
        self.setLayout(self.create_gui())
        self.set_ui_texts()

    def create_gui(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()
        info_group = QGroupBox()
        info_group.setObjectName("infoGroup")
        group_layout = QVBoxLayout()
        name_layout = QHBoxLayout()
        name_label = QLabel()
        name_label.setObjectName("nameLabel")
        name_label_default = QLabel()
        name_label_default.setObjectName("nameLabelDefault")
        author_layout = QHBoxLayout()
        author_label = QLabel()
        author_label.setObjectName("authorLabel")
        author_label_default = QLabel()
        author_label_default.setObjectName("authorLabelDefault")
        version_layout = QHBoxLayout()
        version_label = QLabel()
        version_label.setObjectName("versionLabel")
        version_label_default = QLabel()
        version_label_default.setObjectName("versionLabelDefault")
        github_layout = QHBoxLayout()
        github_label = QLabel()
        github_label.setObjectName("githubLabel")
        github_label_default = QLabel()
        github_label_default.setObjectName("githubLabelDefault")
        github_label_default.setOpenExternalLinks(True)
        github_label_default.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        description_group = QGroupBox()
        description_group.setObjectName("descriptionGroup")
        description_layout = QVBoxLayout()
        description_edit = QTextEdit()
        description_edit.setObjectName("descriptionEdit")
        description_edit.setReadOnly(True)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        button_box.rejected.connect(self.reject)
        name_layout.addWidget(name_label)
        name_layout.addStretch()
        name_layout.addWidget(name_label_default)
        author_layout.addWidget(author_label)
        author_layout.addStretch()
        author_layout.addWidget(author_label_default)
        version_layout.addWidget(version_label)
        version_layout.addStretch()
        version_layout.addWidget(version_label_default)
        github_layout.addWidget(github_label)
        github_layout.addStretch()
        github_layout.addWidget(github_label_default)
        group_layout.addLayout(name_layout)
        group_layout.addLayout(author_layout)
        group_layout.addLayout(version_layout)
        group_layout.addLayout(github_layout)
        info_group.setLayout(group_layout)
        description_layout.addWidget(description_edit)
        description_group.setLayout(description_layout)
        main_layout.addWidget(info_group)
        main_layout.addWidget(description_group)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_texts(self) -> None:
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
                    if isinstance(widget, QGroupBox):
                        widget.setTitle(ui_texts.get(text_key, default_text))
                    elif isinstance(widget, (QLabel, QPushButton)):
                        widget.setText(ui_texts.get(text_key, default_text))
                    elif isinstance(widget, QTextEdit):
                        widget.setPlainText(ui_texts.get(text_key, default_text))
        except Exception as e:
            ui_texts = LanguageProvider.get_ui_texts("errorDialog")
            ErrorHandler.exception_handler(self.__class__.__name__, e, ui_texts=ui_texts, parent=self.parent)