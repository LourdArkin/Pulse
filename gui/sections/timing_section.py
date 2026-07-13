from PySide6.QtWidgets import (
    QCheckBox,
    QLabel,
    QHBoxLayout,
)

from gui.widgets.collapsible_section import CollapsibleSection
from gui.widgets.slider_setting import SliderSetting


class TimingSection(CollapsibleSection):
    def __init__(self, config_manager):
        super().__init__("Natural Behavior")

        self.config = config_manager
        self.loading = False

        self.build_ui()
        self.connect_signals()
        self.load_values()
        self.update_ui()

    def build_ui(self):
        # ---------------- Timing ----------------

        self.description = QLabel(
            "Adds natural variation to make actions less predictable."
        )

        self.description.setWordWrap(True)

        self.description.setStyleSheet("""
            color: gray;
            font-size: 11px;
            margin-bottom: 8px;
        """)

        self.content_layout.addWidget(self.description)

        self.enable_random_timing = QCheckBox(
            "Enable Timing Variation"
        )
        self.content_layout.addWidget(
            self.enable_random_timing
        )

        # ---------------- Variation ----------------

        variation_row = QHBoxLayout()

        variation_label = QLabel("Timing Variation")

        help_label = QLabel("ⓘ")
        help_label.setToolTip(
            """
            <b>Timing Variation</b><br><br>

            Changes the delay between automated actions by a
            small random amount.<br><br>

            <b>0%</b> = Fixed timing<br>
            <b>20%</b> = Small natural variation<br>
            <b>50%</b> = Large natural variation<br><br>

            The average timing remains the same.
            """
        )

        variation_row.addWidget(variation_label)
        variation_row.addWidget(help_label)
        variation_row.addStretch()

        self.content_layout.addLayout(variation_row)

        self.randomness_setting = SliderSetting(
            label="",
            minimum=0,
            maximum=100,
            value=20,
            unit="%",
        )

        self.content_layout.addWidget(
            self.randomness_setting
        )

    def connect_signals(self):
        self.enable_random_timing.toggled.connect(
            self.update_ui
        )

        self.enable_random_timing.toggled.connect(
            self.update_config
        )

        self.randomness_setting.valueChanged.connect(
            self.update_config
        )

    def load_values(self):
        self.loading = True

        timing = self.config.get_active_profile()["timing"]

        self.enable_random_timing.setChecked(
            timing["enabled"]
        )

        self.randomness_setting.setValue(
            timing["randomness"]
        )

        self.loading = False

        print("Timing load:", timing)

    def update_config(self):
        if self.loading:
            return

        print("Timing update_config() called")

        self.config.update_active_profile_section(
            "timing",
            {
                "enabled": self.enable_random_timing.isChecked(),
                "randomness": self.randomness_setting.value(),
            }
        )

    def update_ui(self):
        enabled = self.enable_random_timing.isChecked()

        self.randomness_setting.setEnabled(enabled)