import json
import os
import logging

logger = logging.getLogger("Pulse")  # DEBUG


class ConfigManager:
    """
    Handles loading/saving Pulse configuration.
    Single source of truth for all settings.
    """

    def __init__(self, path=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path = os.path.join(base_dir, "config.json")

        self.data = {}
        self.load()


        logger.info(f"ConfigManager initialized → {self.path}")

        print("ConfigManager ID:", id(self))  # DEBUG


    def load(self):
        if not os.path.exists(self.path):
            self.data = self.default_config()
            self.save()
            return

        with open(self.path, "r") as f:
            self.data = json.load(f)

        logger.info("Configuration loaded")  # DEBUG


    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)

        logger.info("Configuration saved")


    def default_profile(self):
        """Returns the default settings for a new profile."""

        return {
            "mouse": {
                "movement_enabled": True,
                "movement_distance": 10,
                "randomize_distance": False,
                "min_distance": 5,
                "max_distance": 50,
                "movement_interval": 30,
                "clicks_enabled": True,
                "click_interval": 30,
                "click_button": "left"
            },

            "keyboard": {
                "enabled": True,
                "preset": "minimal",
                "interval": 30
            },

            "timing": {
                "enabled": True,
                "randomness": 20
            }
        }


    def default_config(self):
        return {
            "active_profile": "default",
            "profiles": {
                "default": self.default_profile()
            }
        }


    def get_active_profile(self):
        """Returns the currently active profile's settings."""
        name = self.data["active_profile"]
        return self.data["profiles"][name]


    def get_active_profile_name(self):
        """Returns the name of the currently active profile."""
        return self.data["active_profile"]


    def get_profile_names(self):
        """Returns a list of all profile names."""
        return list(self.data["profiles"].keys())
    

    def create_profile(self, name: str):
        """Creates a new profile."""

        if name in self.data["profiles"]:
            logger.warning(f"Profile '{name}' already exists.")
            return False

        self.data["profiles"][name] = self.default_profile()

        self.save()

        logger.info(f"Created profile '{name}'")

        return True
    

    def rename_profile(self, old_name: str, new_name: str):
        """Renames an existing profile."""

        if old_name not in self.data["profiles"]:
            logger.warning(f"Profile '{old_name}' does not exist.")
            return False

        if new_name in self.data["profiles"]:
            logger.warning(f"Profile '{new_name}' already exists.")
            return False

        self.data["profiles"][new_name] = self.data["profiles"].pop(old_name)

        if self.data["active_profile"] == old_name:
            self.data["active_profile"] = new_name

        self.save()

        logger.info(f"Renamed profile '{old_name}' to '{new_name}'")

        return True
    

    def delete_profile(self, name: str):
        """Deletes an existing profile."""

        if name not in self.data["profiles"]:
            logger.warning(f"Profile '{name}' does not exist.")
            return False

        if len(self.data["profiles"]) == 1:
            logger.warning("Cannot delete the last remaining profile.")
            return False

        del self.data["profiles"][name]

        # If the active profile was deleted,
        # switch to the first remaining profile.
        if self.data["active_profile"] == name:
            self.data["active_profile"] = next(iter(self.data["profiles"]))

        self.save()

        logger.info(f"Deleted profile '{name}'")

        return True


    def set_active_profile(self, name):
        self.data["active_profile"] = name
        self.save()
        logger.info(f"Active profile changed to '{name}'")


    def update_active_profile_section(
        self,
        section: str,
        values: dict,
    ):
        """
        Updates multiple values in one section of the active profile.
        Saves only once.
        """

        profile = self.get_active_profile()

        changed = False

        for key, value in values.items():
            if profile[section][key] != value:
                profile[section][key] = value
                logger.info(f"Updated '{section}.{key}' -> {value}")
                changed = True

        if changed:
            self.save()