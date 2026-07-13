from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
)

from gui.widgets.collapsible_section import CollapsibleSection


class HotkeysSection(CollapsibleSection):
    def __init__(self, config_manager):
        super().__init__("Hotkeys")

        self.config = config_manager

        self.build_ui()
        self.connect_signals()
        self.load_values()
        self.update_ui()

    # ---------------- UI ----------------

    def build_ui(self):

        self.enable_hotkeys = QCheckBox("Enable Global Hotkeys")
        self.content_layout.addWidget(self.enable_hotkeys)

        # ---------- Start ----------
        start_layout = QHBoxLayout()

        start_layout.addWidget(QLabel("Start Simulator"))

        self.start_hotkey_button = QPushButton()
        self.start_hotkey_button.setEnabled(False)

        start_layout.addStretch()
        start_layout.addWidget(self.start_hotkey_button)

        self.content_layout.addLayout(start_layout)

        # ---------- Stop ----------
        stop_layout = QHBoxLayout()

        stop_layout.addWidget(QLabel("Stop Simulator"))

        self.stop_hotkey_button = QPushButton()
        self.stop_hotkey_button.setEnabled(False)

        stop_layout.addStretch()
        stop_layout.addWidget(self.stop_hotkey_button)

        self.content_layout.addLayout(stop_layout)

        # ---------- Settings ----------
        settings_layout = QHBoxLayout()

        settings_layout.addWidget(QLabel("Toggle Settings Window"))

        self.settings_hotkey_button = QPushButton()
        self.settings_hotkey_button.setEnabled(False)

        settings_layout.addStretch()
        settings_layout.addWidget(self.settings_hotkey_button)

        self.content_layout.addLayout(settings_layout)

    # ---------------- Signals ----------------

    def connect_signals(self):
        self.enable_hotkeys.toggled.connect(self.update_ui)
        self.enable_hotkeys.toggled.connect(self.update_config)

    # ---------------- Load ----------------

    def load_values(self):
        hotkeys = self.config.get_active_profile()["hotkeys"]

        self.enable_hotkeys.blockSignals(True)

        self.enable_hotkeys.setChecked(hotkeys["enabled"])

        self.start_hotkey_button.setText(hotkeys["start"])
        self.stop_hotkey_button.setText(hotkeys["stop"])
        self.settings_hotkey_button.setText(
            hotkeys["toggle_window"]
        )

        self.enable_hotkeys.blockSignals(False)

        self.update_ui()

        print("Hotkeys load:", hotkeys)

    # ---------------- Config ----------------

    def update_config(self):
        self.config.update_active_profile_section(
            "hotkeys",
            {
                "enabled": self.enable_hotkeys.isChecked(),
                "start": self.start_hotkey_button.text(),
                "stop": self.stop_hotkey_button.text(),
                "toggle_window": self.settings_hotkey_button.text(),
            },
        )

    # ---------------- UI ----------------

    def update_ui(self):
        enabled = self.enable_hotkeys.isChecked()

        self.start_hotkey_button.setEnabled(enabled)
        self.stop_hotkey_button.setEnabled(enabled)
        self.settings_hotkey_button.setEnabled(enabled)