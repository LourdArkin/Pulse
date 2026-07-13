from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QRadioButton,
)

from gui.widgets.collapsible_section import CollapsibleSection
from gui.widgets.slider_setting import SliderSetting


class MouseSection(CollapsibleSection):
    def __init__(self, config_manager):
        super().__init__("Mouse")

        self.config = config_manager
        self.loading = False

        self.build_ui()
        self.load_values()
        self.connect_signals()
        self.update_ui()

    # ---------------- UI ----------------
    def build_ui(self):
        # Mouse Movement
        self.enable_mouse_movement = QCheckBox("Enable Tiny Mouse Movement")
        self.content_layout.addWidget(self.enable_mouse_movement)

        self.randomize_distance = QCheckBox("Randomize Movement Distance")
        self.content_layout.addWidget(self.randomize_distance)

        self.min_distance_setting = SliderSetting(
            label="Minimum Movement Distance",
            minimum=1,
            maximum=200,
            value=10,
            unit="pixels",
        )
        self.content_layout.addWidget(self.min_distance_setting)

        self.max_distance_setting = SliderSetting(
            label="Maximum Movement Distance",
            minimum=1,
            maximum=200,
            value=30,
            unit="pixels",
        )
        self.content_layout.addWidget(self.max_distance_setting)

        self.distance_setting = SliderSetting(
            label="Movement Distance",
            minimum=1,
            maximum=200,
            value=10,
            unit="pixels",
        )
        self.content_layout.addWidget(self.distance_setting)

        self.movement_interval_setting = SliderSetting(
            label="Average Time Between Mouse Movements",
            minimum=5,
            maximum=300,
            value=30,
            unit="seconds",
        )
        self.content_layout.addWidget(self.movement_interval_setting)

        # Mouse Clicks
        self.enable_random_clicks = QCheckBox("Enable Random Mouse Clicks")
        self.content_layout.addWidget(self.enable_random_clicks)

        self.click_interval_setting = SliderSetting(
            label="Average Time Between Clicks",
            minimum=5,
            maximum=300,
            value=30,
            unit="seconds",
        )
        self.content_layout.addWidget(self.click_interval_setting)

        self.left_click_radio = QRadioButton("Left Click")
        self.right_click_radio = QRadioButton("Right Click")

        self.left_click_radio.setChecked(True)

        self.click_button_group = QButtonGroup(self)
        self.click_button_group.addButton(self.left_click_radio)
        self.click_button_group.addButton(self.right_click_radio)

        self.content_layout.addWidget(self.left_click_radio)
        self.content_layout.addWidget(self.right_click_radio)

    # ---------------- Load ----------------
    def load_values(self):
        self.loading = True

        mouse = self.config.get_active_profile()["mouse"]

        self.enable_mouse_movement.setChecked(mouse["movement_enabled"])
        self.randomize_distance.setChecked(mouse["randomize_distance"])

        self.min_distance_setting.setValue(mouse["min_distance"])
        self.max_distance_setting.setValue(mouse["max_distance"])
        self.distance_setting.setValue(mouse["movement_distance"])
        self.movement_interval_setting.setValue(mouse["movement_interval"])

        self.enable_random_clicks.setChecked(mouse["clicks_enabled"])
        self.click_interval_setting.setValue(mouse["click_interval"])

        if mouse["click_button"] == "left":
            self.left_click_radio.setChecked(True)
        else:
            self.right_click_radio.setChecked(True)

        self.loading = False

        print("Mouse load:", mouse)

    # ---------------- Signals ----------------
    def connect_signals(self):
        self.enable_mouse_movement.toggled.connect(self.update_ui)
        self.enable_random_clicks.toggled.connect(self.update_ui)
        self.randomize_distance.toggled.connect(self.update_ui)

        self.enable_mouse_movement.toggled.connect(self.update_config)
        self.enable_random_clicks.toggled.connect(self.update_config)
        self.randomize_distance.toggled.connect(self.update_config)

        self.distance_setting.valueChanged.connect(self.update_config)
        self.movement_interval_setting.valueChanged.connect(self.update_config)
        self.click_interval_setting.valueChanged.connect(self.update_config)

        self.min_distance_setting.valueChanged.connect(self.update_config)
        self.max_distance_setting.valueChanged.connect(self.update_config)

        self.left_click_radio.toggled.connect(self.update_config)
        self.right_click_radio.toggled.connect(self.update_config)

    # ---------------- Config ----------------
    def update_config(self):
        if self.loading:
            return

        print("Mouse update_config() called")

        self.config.update_active_profile_section(
            "mouse",
            {
                "movement_enabled": self.enable_mouse_movement.isChecked(),
                "randomize_distance": self.randomize_distance.isChecked(),
                "min_distance": self.min_distance_setting.value(),
                "max_distance": self.max_distance_setting.value(),
                "movement_distance": self.distance_setting.value(),
                "movement_interval": self.movement_interval_setting.value(),
                "clicks_enabled": self.enable_random_clicks.isChecked(),
                "click_interval": self.click_interval_setting.value(),
                "click_button": (
                    "left"
                    if self.left_click_radio.isChecked()
                    else "right"
                ),
            },
        )

    # ---------------- UI state ----------------
    def update_ui(self):
        movement_enabled = self.enable_mouse_movement.isChecked()
        clicks_enabled = self.enable_random_clicks.isChecked()
        random_enabled = movement_enabled and self.randomize_distance.isChecked()

        # Movement controls
        self.distance_setting.setEnabled(movement_enabled)
        self.movement_interval_setting.setEnabled(movement_enabled)
        self.randomize_distance.setEnabled(movement_enabled)

        # Random distance controls
        self.min_distance_setting.setEnabled(random_enabled)
        self.max_distance_setting.setEnabled(random_enabled)

        # Click controls
        self.click_interval_setting.setEnabled(clicks_enabled)
        self.left_click_radio.setEnabled(clicks_enabled)
        self.right_click_radio.setEnabled(clicks_enabled)