import keyboard
import logging

logger = logging.getLogger("Pulse")


class HotkeyManager:
    def __init__(self, config, app):
        self.config = config
        self.app = app
        self.registered = []

    def register(self):
        logger.info("Registering global hotkeys...")

        hotkeys = self.config.get_active_profile()["hotkeys"]

        if not hotkeys["enabled"]:
            logger.info("Global hotkeys are disabled.")
            return

        # Start
        keyboard.add_hotkey(
            hotkeys["start"],
            self.app.start_simulator,
        )

        logger.info(
            f"Registered Start Hotkey: {hotkeys['start']}"
        )

        # Stop
        keyboard.add_hotkey(
            hotkeys["stop"],
            self.app.stop_simulator,
        )

        logger.info(
            f"Registered Stop Hotkey: {hotkeys['stop']}"
        )

        # Toggle Settings
        keyboard.add_hotkey(
            hotkeys["toggle_window"],
            self.app.toggle_settings,
        )

        logger.info(
            f"Registered Toggle Hotkey: {hotkeys['toggle_window']}"
        )

    def unregister(self):
        logger.info("Removing global hotkeys...")

        keyboard.clear_all_hotkeys()
        self.registered.clear()

    def reload(self):
        self.unregister()
        self.register()