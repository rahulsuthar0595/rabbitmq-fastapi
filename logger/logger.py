import logging.config
import os

LOG_DIR = "logs/"
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "key_value": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": f"{LOG_DIR}/app.log",
            "formatter": "key_value",
        }
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


