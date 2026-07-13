from PySide6.QtWidgets import (
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QInputDialog
)

from gui.widgets.collapsible_section import CollapsibleSection


class ProfileSection(CollapsibleSection):
    def __init__(self, settings_window):
        super().__init__("Profiles")

        self.settings_window = settings_window
        self.config = settings_window.app.config

        self.build_ui()
        self.refresh_profiles()
        self.connect_signals()

        print("ProfileSection Config ID:", id(self.config))


    def connect_signals(self):
        self.new_button.clicked.connect(self.create_profile)
        self.rename_button.clicked.connect(self.rename_profile)
        self.delete_button.clicked.connect(self.delete_profile)
        self.profile_dropdown.currentTextChanged.connect(self.profile_changed)


    def build_ui(self):
        self.profile_dropdown = QComboBox()
        self.content_layout.addWidget(self.profile_dropdown)

        button_layout = QHBoxLayout()

        self.new_button = QPushButton("New")
        self.rename_button = QPushButton("Rename")
        self.delete_button = QPushButton("Delete")

        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.rename_button)
        button_layout.addWidget(self.delete_button)

        self.content_layout.addLayout(button_layout)


    def refresh_profiles(self):
        current = self.config.get_active_profile_name()

        self.profile_dropdown.blockSignals(True)

        self.profile_dropdown.clear()
        self.profile_dropdown.addItems(self.config.get_profile_names())

        self.profile_dropdown.setCurrentText(current)

        self.profile_dropdown.blockSignals(False)


    def profile_changed(self, name):
        if not name:
            return

        self.config.set_active_profile(name)

        # 🔥 KEY FIX: sync OTHER dropdown too
        self.settings_window.profile_selector.refresh_profiles()

        self.settings_window.reload_profile()


    def create_profile(self):
        name, ok = QInputDialog.getText(
            self,
            "New Profile",
            "Profile name:"
        )

        if not ok or not name.strip():
            return

        name = name.strip()

        if self.config.create_profile(name):
            self.refresh_profiles()

            # 🔥 KEY FIX
            self.settings_window.profile_selector.refresh_profiles()

            self.profile_dropdown.setCurrentText(name)


    def rename_profile(self):
        old_name = self.profile_dropdown.currentText()

        new_name, ok = QInputDialog.getText(
            self,
            "Rename Profile",
            "New profile name:",
            text=old_name
        )

        if not ok or not new_name.strip():
            return

        new_name = new_name.strip()

        if self.config.rename_profile(old_name, new_name):
            self.refresh_profiles()

            # 🔥 KEY FIX
            self.settings_window.profile_selector.refresh_profiles()

            self.profile_dropdown.setCurrentText(new_name)


    def select_profile(self, name):
        self.profile_dropdown.setCurrentText(name)

    
    def delete_profile(self):
        name = self.profile_dropdown.currentText()

        if not name:
            return

        # safety: prevent deleting last profile
        if len(self.config.get_profile_names()) <= 1:
            print("Cannot delete last profile.")
            return

        if self.config.delete_profile(name):
            self.settings_window.reload_profile()
            self.settings_window.profile_selector.refresh_profiles()
            self.refresh_profiles()