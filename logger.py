import os
import time
import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    """Sets up logging with both console and file handlers."""
    log_dir = "/app/logs"
    os.makedirs(log_dir, exist_ok=True)

    log_filename = f"pc_builder_app_{time.strftime('%Y%m%d')}.log"
    file_path = os.path.join(log_dir, log_filename)

    logger = logging.getLogger(f"PcBuilderApp")

    # Fetch log level from environment variable, default to DEBUG if not set or invalid
    log_level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_level = getattr(logging, log_level_name, logging.DEBUG)

    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(file_path, maxBytes=1024 * 1024 * 5, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger