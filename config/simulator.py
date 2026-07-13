import logging
import random
import threading
import time

logger = logging.getLogger("Pulse")


class Simulator:
    def __init__(self, config_manager, keyboard_engine, mouse_engine):
        self.config = config_manager
        self.keyboard_engine = keyboard_engine
        self.mouse_engine = mouse_engine

        self.running = False
        self.thread = None
        self.stop_event = threading.Event()


    def start(self):
        if self.running:
            return

        self.running = True
        self.stop_event.clear()

        now = time.monotonic()

        mouse = self.get_mouse_config()
        keyboard = self.config.get_active_profile()["keyboard"]

        self.next_mouse_move = now + self.get_randomized_interval(
            mouse["movement_interval"]
        )

        self.next_mouse_click = now + self.get_randomized_interval(
            mouse["click_interval"]
        )

        self.next_keyboard_action = now + self.get_randomized_interval(
            keyboard["interval"]
        )

        self.thread = threading.Thread(target=self.run_loop, daemon=True)
        self.thread.start()

        logger.info("Simulator started.")

    def stop(self):
        if not self.running:
            return

        self.running = False
        self.stop_event.set()

        logger.info("Stopping simulator...")

        if self.thread is not None:
            self.thread.join(timeout=2)

        logger.info("Simulator thread joined.")

    def run_loop(self):
        while self.running:

            keyboard = self.get_keyboard_config()
            mouse = self.get_mouse_config()

            if not keyboard["enabled"]:
                if self.stop_event.wait(0.1):
                    break
                continue

            allowed_keys = self.keyboard_engine.get_allowed_keys()

            if not allowed_keys:
                logger.warning("No allowed keys found in the active profile.")
                if self.stop_event.wait(0.1):
                    break
                continue

            now = time.monotonic()

            # ---------------- Keyboard ----------------
            if now >= self.next_keyboard_action:

                key = random.choice(allowed_keys)
                self.keyboard_engine.press(key)

                self.next_keyboard_action = (
                    now +
                    self.get_randomized_interval(
                        keyboard["interval"]
                    )
                )

            # ---------------- Mouse Movement ----------------
            if mouse["movement_enabled"]:
                if now >= self.next_mouse_move:

                    self.mouse_engine.move()

                    self.next_mouse_move = (
                        now +
                        self.get_randomized_interval(
                            mouse["movement_interval"]
                        )
                    )

            # ---------------- Mouse Click ----------------
            if mouse["clicks_enabled"]:
                if now >= self.next_mouse_click:

                    self.mouse_engine.click(
                        mouse["click_button"]
                    )

                    self.next_mouse_click = (
                        now +
                        self.get_randomized_interval(
                            mouse["click_interval"]
                        )
                    )

            # Small sleep to prevent high CPU usage
            if self.stop_event.wait(0.01):
                break

    def get_mouse_config(self):
        return self.config.get_active_profile()["mouse"]
    
    def get_keyboard_config(self):
        return self.config.get_active_profile()["keyboard"]
    
    def get_randomized_interval(self, base_interval):
        timing = self.config.get_active_profile()["timing"]

        if not timing["enabled"]:
            return base_interval

        variation = timing["randomness"] / 100

        offset = base_interval * variation

        return random.uniform(
            base_interval - offset,
            base_interval + offset
        )