from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)


class HotkeyRow(QWidget):
    """
    Reusable hotkey setting.

    Example:

        Start Simulator

        [ Ctrl + Shift + S ]   [ Change ]
    """

    changeRequested = Signal()

    def __init__(self, title: str, shortcut: str = ""):
        super().__init__()

        self.build_ui(title, shortcut)

    def build_ui(self, title: str, shortcut: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # ---------------- Title ----------------

        self.title_label = QLabel(title)
        layout.addWidget(self.title_label)

        # ---------------- Buttons ----------------

        row = QHBoxLayout()

        self.shortcut_button = QPushButton(shortcut)
        self.shortcut_button.setEnabled(False)

        self.change_button = QPushButton("Change")

        row.addWidget(self.shortcut_button)
        row.addWidget(self.change_button)

        layout.addLayout(row)

        # ---------------- Signals ----------------

        self.change_button.clicked.connect(
            self.changeRequested.emit
        )

    def setShortcut(self, shortcut: str):
        self.shortcut_button.setText(shortcut)

    def shortcut(self):
        return self.shortcut_button.text()