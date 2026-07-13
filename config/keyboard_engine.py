import string
import logging
import pyautogui

logger = logging.getLogger("Pulse")  # DEBUG


class KeyboardEngine:
    """
    Converts keyboard presets into actual usable key pools.
    """

    def __init__(self, config_manager):
        self.config = config_manager
        logger.info("KeyboardEngine initialized")

    def get_allowed_keys(self):
        profile = self.config.get_active_profile()
        preset = profile["keyboard"]["preset"]

        if preset == "minimal":
            return list(string.ascii_lowercase)

        elif preset == "standard":
            return list(string.ascii_lowercase) + list(string.digits)

        elif preset == "expanded":
            return (
                list(string.ascii_lowercase)
                + list(string.digits)
                + list(" .,;'-_/")
            )

        elif preset == "custom":
            # For now fallback (we'll build UI later)
            return list(string.ascii_lowercase)

        # safety fallback
        return list(string.ascii_lowercase)
    
    def press(self, key: str):
        """Presses a single keyboard key."""
        pyautogui.press(key)