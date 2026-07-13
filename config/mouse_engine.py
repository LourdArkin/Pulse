import random
import pyautogui
import time
import math
import logging

logger = logging.getLogger("Pulse")  # DEBUG

class MouseEngine:
    def __init__(self, config):
        self.config = config

    def move(self):
        mouse = self.get_mouse_config()
        if mouse["randomize_distance"]:
            distance = random.randint(mouse["min_distance"], mouse["max_distance"])
        else:
            distance = mouse["movement_distance"]
        current_x, current_y = pyautogui.position()

        target_x = current_x + random.randint(-distance, distance)
        target_y = current_y + random.randint(-distance, distance)

        self.smooth_move_to(target_x, target_y)

    def smooth_move_to(self, target_x: int, target_y: int):
        start_x, start_y = pyautogui.position()

        dx = target_x - start_x
        dy = target_y - start_y

        steps = 30

        previous_x = start_x
        previous_y = start_y

        for i in range(1, steps + 1):

            t = i / steps
            eased = (1 - math.cos(math.pi * t)) / 2

            current_x = start_x + dx * eased
            current_y = start_y + dy * eased

            pyautogui.moveRel(
                current_x - previous_x,
                current_y - previous_y
            )

            previous_x = current_x
            previous_y = current_y

            time.sleep(0.005)

    def click(self, button: str):
        """Performs a mouse click."""

        logger.info(f"Mouse click triggered: {button} button")  # DEBUG
        pyautogui.click(button=button)

    def get_mouse_config(self):
        return self.config.get_active_profile()["mouse"]