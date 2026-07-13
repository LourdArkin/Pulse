from PySide6.QtWidgets import (
    QCheckBox,
    QPushButton,
)

from gui.widgets.collapsible_section import CollapsibleSection
from gui.widgets.hotkey_row import HotkeyRow


class HotkeysSection(CollapsibleSection):
    def __init__(self):
        super().__init__("Hotkeys")

        self.build_ui()

    def build_ui(self):

        # ---------------- Enable ----------------

        self.enable_hotkeys = QCheckBox(
            "Enable Global Hotkeys"
        )

        self.content_layout.addWidget(
            self.enable_hotkeys
        )

        # ---------------- Hotkeys ----------------

        self.start_hotkey = HotkeyRow(
            "Start Simulator",
            "Ctrl + Shift + S"
        )

        self.stop_hotkey = HotkeyRow(
            "Stop Simulator",
            "Ctrl + Shift + X"
        )

        self.toggle_hotkey = HotkeyRow(
            "Toggle Window",
            "Ctrl + Shift + P"
        )

        self.content_layout.addWidget(self.start_hotkey)
        self.content_layout.addWidget(self.stop_hotkey)
        self.content_layout.addWidget(self.toggle_hotkey)

        # ---------------- Defaults ----------------

        self.restore_button = QPushButton(
            "Restore Defaults"
        )

        self.content_layout.addWidget(
            self.restore_button
        )