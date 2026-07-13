import logging
import os


def setup_logger():
    # Create logs folder if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("Pulse")

    # Prevent duplicate handlers if called multiple times
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S"
    )

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Log file
    file_handler = logging.FileHandler(
        "logs/pulse.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger