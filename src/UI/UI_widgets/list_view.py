from PyQt6.QtWidgets import QListView


class ListView(QListView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("listView")