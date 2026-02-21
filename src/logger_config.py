import logging
import json
import os
from datetime import datetime

LOG_DIR = "reports"
LOG_FILE = os.path.join(LOG_DIR, "sentinel.log")


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if hasattr(record, "stage"):
            log_record["stage"] = record.stage

        return json.dumps(log_record)


def get_logger():
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("sentinel_logger")
    logger.setLevel(logging.INFO)

    
    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(JSONFormatter())

    logger.addHandler(file_handler)

    return logger
