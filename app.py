from config.config_manager import ConfigManager
from config.keyboard_engine import KeyboardEngine
from config.simulator import Simulator

from gui.settings_window import SettingsWindow
from tray.tray_manager import TrayManager
from config.mouse_engine import MouseEngine

import logging

logger = logging.getLogger("Pulse")  # DEBUG = logging.getLogger("Pulse")  # DEBUG


class PulseApp:
    def __init__(self):
        # -----------------------------
        # CONFIG SYSTEM
        # -----------------------------
        self.config = ConfigManager()
        

        # -----------------------------
        # CORE ENGINE
        # -----------------------------
        self.keyboard_engine = KeyboardEngine(self.config)
        self.mouse_engine = MouseEngine(self.config)
        self.simulator = Simulator(
            self.config,
            self.keyboard_engine,
            self.mouse_engine
        )

        # -----------------------------
        # APPLICATION STATE
        # -----------------------------
        self.is_running = False

        # -----------------------------
        # UI
        # -----------------------------
        self.settings_window = SettingsWindow(self)

        # -----------------------------
        # SYSTEM TRAY
        # -----------------------------
        self.tray = TrayManager(self)

    # -----------------------------
    # UI CONTROL
    # -----------------------------
    def show_settings(self):
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def hide_settings(self):
        self.settings_window.hide()

    # -----------------------------
    # APP LIFECYCLE
    # -----------------------------
    def run(self):
        logger.info("PulseApp is running...")  # DEBUG

        # IMPORTANT: single, stable UI entry point
        self.show_settings()

    # -----------------------------
    # SIMULATOR CONTROL
    # -----------------------------
    def start_simulator(self):
        if self.is_running:
            return
        
        
        logger.info("Starting simulator...")  # DEBUG
        self.simulator.start()
        self.is_running = True
        self.settings_window.update_status(True)
        self.settings_window.update_buttons(True)
        self.tray.update_state(True)

    def stop_simulator(self):
        if not self.is_running:
            return

        logger.info("Stopping simulator...")  # DEBUG
        self.simulator.stop()
        self.is_running = False
        self.settings_window.update_status(False)
        self.settings_window.update_buttons(False)
        self.tray.update_state(False)

        
    def simulator_running(self):
        return self.is_running
    