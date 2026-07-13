from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel

from gui.sections.keyboard_section import KeyboardSection
from gui.sections.mouse_section import MouseSection
from gui.widgets.status_card import StatusCard
from gui.widgets.collapsible_section import CollapsibleSection
from gui.widgets.profile_selector import ProfileSelector
from gui.sections.profile_section import ProfileSection
from gui.sections.timing_section import TimingSection


class SettingsWindow(QWidget):
    def __init__(self, app):
        super().__init__()

        # Store full app reference (IMPORTANT)
        self.app = app

        self.setWindowTitle("Pulse")

        from gui.theme import WINDOW_WIDTH, WINDOW_HEIGHT
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.build_ui()


    def build_ui(self):
        layout = QVBoxLayout(self)

        # ---------------- Status ----------------
        self.status_card = StatusCard()
        layout.addWidget(self.status_card)

        self.profile_selector = ProfileSelector(
            self.app.config, self
        )
        layout.addWidget(self.profile_selector)

        #----------------- Profile Section ----------------
        self.profile_section = ProfileSection(self)
        layout.addWidget(self.profile_section)

        # ---------------- Sections ----------------
        self.mouse_section = MouseSection(self.app.config)
        self.keyboard_section = KeyboardSection(self.app.config)
        self.timing_section = TimingSection(self.app.config)

        layout.addWidget(self.mouse_section)
        layout.addWidget(self.keyboard_section)
        layout.addWidget(self.timing_section)

        # Placeholder sections

        layout.addWidget(CollapsibleSection("Startup"))
        layout.addWidget(QLabel("Coming Soon..."))

        layout.addWidget(CollapsibleSection("Hotkeys"))
        layout.addWidget(QLabel("Coming Soon..."))

        layout.addStretch()

        # ---------------- Save Button ----------------
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.app.config.save)
        layout.addWidget(save_button)

        # ---------------- Simulator Controls ----------------
        self.start_button = QPushButton("Start Simulator")
        self.stop_button = QPushButton("Stop Simulator")

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.start_button.clicked.connect(self.app.start_simulator)
        self.stop_button.clicked.connect(self.app.stop_simulator)

        # Initial button states
        self.update_buttons(False)


    def update_status(self, running: bool):
        
        if running:
            self.status_card.set_status("🟢 Running")
        else:
            self.status_card.set_status("🔴 Stopped")


    def update_buttons(self, running: bool):
        self.start_button.setEnabled(not running)
        self.stop_button.setEnabled(running)


    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.hide()


    def reload_profile(self):
        # IMPORTANT: prevent UI signal interference during reload
        self.mouse_section.blockSignals(True)
        self.keyboard_section.blockSignals(True)
        self.timing_section.blockSignals(True)

        try:
            # 1. Load values from active profile
            self.mouse_section.load_values()
            self.keyboard_section.load_values()
            self.timing_section.load_values()

            print(self.app.config.get_active_profile())

            # 2. Apply UI state AFTER values are loaded
            self.mouse_section.update_ui()
            self.keyboard_section.update_ui()
            self.timing_section.update_ui()

        finally:
            # ALWAYS re-enable signals
            self.mouse_section.blockSignals(False)
            self.keyboard_section.blockSignals(False)
            self.timing_section.blockSignals(False)
    
    def reload_all_profiles(self):
        self.profile_selector.refresh_profiles()
        self.profile_section.refresh_profiles()