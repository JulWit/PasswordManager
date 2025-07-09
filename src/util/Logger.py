import logging
from pathlib import Path

from src import ROOT_DIR

# Log-Verzeichnis
LOG_DIR = Path(ROOT_DIR) / "log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log-Format
LOG_FORMAT = "%(asctime)-15s %(module)-25s %(levelname)-8s %(message)s"
DATE_FORMAT = "%d.%m.%y %H:%M"
LOG_FILE = LOG_DIR / "PasswordManager.log"

# Create root logger and prevent duplicate handlers
logger = logging.getLogger("PasswordManager")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # File handler
    file_handler = logging.FileHandler(LOG_FILE, mode="a+", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(console_handler)

# don't propagate log messages to root logger
logger.propagate = False
