import sys
from PySide6.QtWidgets import QApplication

from app import PulseApp

from config.logger import setup_logger


def main():
    # Create Qt application (REQUIRED for UI + tray)
    app = QApplication(sys.argv)

    # Setup logger
    logger = setup_logger()
    logger.info("Pulse starting...") 

    # Create and run your app
    pulse = PulseApp()
    pulse.run()

    # Start Qt event loop (THIS keeps window + tray alive)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()