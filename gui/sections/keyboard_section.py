from PySide6.QtWidgets import QRadioButton, QVBoxLayout, QButtonGroup, QCheckBox

from gui.widgets.collapsible_section import CollapsibleSection
from gui.widgets.slider_setting import SliderSetting


class KeyboardSection(CollapsibleSection):
    def __init__(self, config_manager):
        super().__init__("Keyboard")

        self.config = config_manager
        self.loading = False

        self.build_ui()
        self.load_values()
        self.connect_signals()
        self.update_ui()

    def build_ui(self):
        self.layout = QVBoxLayout()

        self.preset_group = QButtonGroup(self)

        # ---------------- Enable ----------------
        self.enable_keyboard = QCheckBox("Enable Keyboard")
        self.content_layout.addWidget(self.enable_keyboard)

        # ---------------- Interval ----------------
        self.interval_setting = SliderSetting(
            label="Average Time Between Key Presses",
            minimum=5,
            maximum=300,
            value=30,
            unit="seconds",
        )
        self.content_layout.addWidget(self.interval_setting)

        # ---------------- Presets ----------------
        self.minimal = QRadioButton("Minimal (A–Z)")
        self.standard = QRadioButton("Standard (A–Z + 0–9)")
        self.expanded = QRadioButton("Expanded (+ symbols)")
        self.custom = QRadioButton("Custom (advanced)")

        self.preset_group.addButton(self.minimal)
        self.preset_group.addButton(self.standard)
        self.preset_group.addButton(self.expanded)
        self.preset_group.addButton(self.custom)

        self.content_layout.addWidget(self.minimal)
        self.content_layout.addWidget(self.standard)
        self.content_layout.addWidget(self.expanded)
        self.content_layout.addWidget(self.custom)

    def load_values(self):
        self.loading = True

        keyboard = self.config.get_active_profile()["keyboard"]

        self.enable_keyboard.setChecked(keyboard["enabled"])
        self.interval_setting.setValue(keyboard["interval"])

        preset = keyboard["preset"]

        if preset == "minimal":
            self.minimal.setChecked(True)
        elif preset == "standard":
            self.standard.setChecked(True)
        elif preset == "expanded":
            self.expanded.setChecked(True)
        else:
            self.custom.setChecked(True)

        self.loading = False

        print("Keyboard load:", keyboard)

    def connect_signals(self):
        self.enable_keyboard.toggled.connect(self.update_ui)
        self.enable_keyboard.toggled.connect(self.update_config)

        self.interval_setting.valueChanged.connect(self.update_config)

        self.minimal.toggled.connect(self.update_config)
        self.standard.toggled.connect(self.update_config)
        self.expanded.toggled.connect(self.update_config)
        self.custom.toggled.connect(self.update_config)

    def update_config(self):
        if self.loading:
            return

        print("Keyboard update_config() called")

        keyboard = self.config.get_active_profile()["keyboard"]

        keyboard["enabled"] = self.enable_keyboard.isChecked()
        keyboard["interval"] = self.interval_setting.value()

        if self.minimal.isChecked():
            keyboard["preset"] = "minimal"
        elif self.standard.isChecked():
            keyboard["preset"] = "standard"
        elif self.expanded.isChecked():
            keyboard["preset"] = "expanded"
        elif self.custom.isChecked():
            keyboard["preset"] = "custom"

        self.config.save()

    def update_ui(self):
        enabled = self.enable_keyboard.isChecked()

        self.interval_setting.setEnabled(enabled)
        self.minimal.setEnabled(enabled)
        self.standard.setEnabled(enabled)
        self.expanded.setEnabled(enabled)
        self.custom.setEnabled(enabled)