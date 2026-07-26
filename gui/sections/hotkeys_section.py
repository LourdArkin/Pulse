from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
)

from gui.widgets.collapsible_section import CollapsibleSection
from PySide6.QtCore import Qt


class HotkeysSection(CollapsibleSection):
    def __init__(self, app):
        super().__init__("Hotkeys")

        self.app = app
        self.config = app.config

        self.recording = None
        self.current_modifiers = Qt.KeyboardModifier.NoModifier

        self.build_ui()
        self.connect_signals()
        self.load_values()
        self.update_ui()

    # ---------------- UI ----------------

    def build_ui(self):

        # ---------- Start ----------
        # Enable hotkeys
        self.enable_hotkeys = QCheckBox("Enable Global Hotkeys")
        self.content_layout.addWidget(self.enable_hotkeys)
        
        start_layout = QHBoxLayout()

        start_layout.addWidget(QLabel("Start Simulator"))

        self.start_hotkey_label = QLabel()

        start_layout.addStretch()
        start_layout.addWidget(self.start_hotkey_label)

        self.start_hotkey_button = QPushButton("Change")
        self.start_hotkey_button.setEnabled(False)

        start_layout.addWidget(self.start_hotkey_button)

        self.content_layout.addLayout(start_layout)

        # ---------- Stop ----------
        stop_layout = QHBoxLayout()

        stop_layout.addWidget(QLabel("Stop Simulator"))

        self.stop_hotkey_label = QLabel()

        stop_layout.addStretch()
        stop_layout.addWidget(self.stop_hotkey_label)

        self.stop_hotkey_button = QPushButton("Change")
        self.stop_hotkey_button.setEnabled(False)

        stop_layout.addWidget(self.stop_hotkey_button)\
        
        self.content_layout.addLayout(stop_layout)

        # ---------- Settings ----------
        settings_layout = QHBoxLayout()

        settings_layout.addWidget(QLabel("Toggle Settings Window"))

        self.settings_hotkey_label = QLabel()

        settings_layout.addStretch()
        settings_layout.addWidget(self.settings_hotkey_label)

        self.settings_hotkey_button = QPushButton("Change")
        self.settings_hotkey_button.setEnabled(False)

        settings_layout.addWidget(self.settings_hotkey_button)

        self.content_layout.addLayout(settings_layout)

    # ---------------- Signals ----------------

    def connect_signals(self):
        self.enable_hotkeys.toggled.connect(self.update_ui)
        self.enable_hotkeys.toggled.connect(self.update_config)

        self.start_hotkey_button.clicked.connect(
            self.record_start_hotkey
        )

        self.stop_hotkey_button.clicked.connect(
            self.record_stop_hotkey
        )

        self.settings_hotkey_button.clicked.connect(
            self.record_settings_hotkey
        )

    # ---------------- Load ----------------

    def load_values(self):
        hotkeys = self.config.get_active_profile()["hotkeys"]

        self.enable_hotkeys.blockSignals(True)

        self.enable_hotkeys.setChecked(hotkeys["enabled"])

        self.start_hotkey_label.setText(hotkeys["start"])
        self.stop_hotkey_label.setText(hotkeys["stop"])

        self.settings_hotkey_label.setText(
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
                "start": self.start_hotkey_label.text(),
                "stop": self.stop_hotkey_label.text(),
                "toggle_window": self.settings_hotkey_label.text(), 
            },
        )

        self.app.hotkey_manager.reload()

    # ---------------- UI ----------------

    def update_ui(self):
        enabled = self.enable_hotkeys.isChecked()

        self.start_hotkey_button.setEnabled(enabled)
        self.stop_hotkey_button.setEnabled(enabled)
        self.settings_hotkey_button.setEnabled(enabled)

    def record_start_hotkey(self):
        self.recording = "start"
        self.start_hotkey_button.setText("Recording...")
        self.setFocus()


    def record_stop_hotkey(self):
        self.recording = "stop"
        self.stop_hotkey_button.setText("Recording...")
        self.setFocus()


    def record_settings_hotkey(self):
        self.recording = "settings"
        self.settings_hotkey_button.setText("Recording...")
        self.setFocus()

    def keyPressEvent(self, event):
        if self.recording is None:
            super().keyPressEvent(event)
            return

        key = event.key()

        # Ignore modifier keys by themselves
        if key in (
            Qt.Key.Key_Control,
            Qt.Key.Key_Shift,
            Qt.Key.Key_Alt,
            Qt.Key.Key_Meta,
        ):
            return

        parts = []

        modifiers = event.modifiers()

        if modifiers & Qt.KeyboardModifier.ControlModifier:
            parts.append("Ctrl")

        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            parts.append("Shift")

        if modifiers & Qt.KeyboardModifier.AltModifier:
            parts.append("Alt")

        if modifiers & Qt.KeyboardModifier.MetaModifier:
            parts.append("Win")

        # Convert the key into readable text
        # Letters
        if Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
            key_text = chr(key)

        # Numbers
        elif Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
            key_text = chr(key)

        # Everything else
        else:
            key_name = Qt.Key(key).name

            if key_name.startswith("Key_"):
                key_name = key_name[4:]

            key_text = key_name

        parts.append(key_text)

        hotkey = "+".join(parts)

        if self.recording == "start":
            self.start_hotkey_label.setText(hotkey)

        elif self.recording == "stop":
            self.stop_hotkey_label.setText(hotkey)

        elif self.recording == "settings":
            self.settings_hotkey_label.setText(hotkey)

        self.recording = None

        self.update_config()

        self.start_hotkey_button.setText("Change")
        self.stop_hotkey_button.setText("Change")
        self.settings_hotkey_button.setText("Change")