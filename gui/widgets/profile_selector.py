from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox


class ProfileSelector(QWidget):
    def __init__(self, config, window):
        super().__init__()

        self.config = config
        self.window = window

        layout = QHBoxLayout(self)

        self.label = QLabel("Profile")
        self.dropdown = QComboBox()

        layout.addWidget(self.label)
        layout.addWidget(self.dropdown)

        self.refresh_profiles()

        self.dropdown.currentTextChanged.connect(self.on_profile_changed)

    def refresh_profiles(self):
        self.dropdown.blockSignals(True)

        self.dropdown.clear()

        profiles = self.config.get_profile_names()
        self.dropdown.addItems(profiles)

        active = self.config.get_active_profile_name()
        self.dropdown.setCurrentText(active)

        self.dropdown.blockSignals(False)

    def on_profile_changed(self, profile_name):
        if not profile_name:
            return

        # switch profile
        self.config.set_active_profile(profile_name)

        # refresh FULL UI (single source of truth)
        self.window.reload_profile()