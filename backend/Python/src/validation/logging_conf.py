import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)s |%(message)s")

def SetupLogging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(
        f"{LOG_DIR}/app.log",
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8"
    )

    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)
