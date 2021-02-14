import logging
from pathlib import Path

from src.__main__ import ROOT_DIR


def setup_logger(name: str) -> logging.Logger:
    logging_format = "%(asctime)-15s %(module)-25s %(levelname)-8s %(message)s"
    date_format = "%d.%m.%y %H:%M"

    # Ordner für Log-Datein erstellen, falls nicht vorhanden
    Path(ROOT_DIR + "/log/").mkdir(parents=True, exist_ok=True)

    logging.basicConfig(level=logging.DEBUG,
                        format=logging_format,
                        datefmt=date_format,
                        filename=ROOT_DIR + "/log/PasswordManager.log",
                        filemode="a+")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(logging_format)
    formatter.datefmt = date_format
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(console_handler)
    return logger
