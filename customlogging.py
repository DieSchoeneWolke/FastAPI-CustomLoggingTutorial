import getpass
import json
import logging


class UserFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:
        setattr(record, "user", getpass.getuser())
        return True


class CustomFormatter(logging.Formatter):

    def __init__(self):
        super().__init__()

    def formatMessage(self, record: logging.LogRecord) -> str:
        super().formatMessage(record)

        log_record = {
            "message": record.message,
            "level": record.levelname,
            "pathName": record.pathname,
            "lineNumber": record.lineno,
            "threadId": record.thread,
            "user": record.user
        }

        return json.dumps(log_record)

logging_config: dict = {
    "version": 1,
    "filters": {"user": {"()": lambda: UserFilter()}},
    "formatters": {
        "customformatter": {"()": lambda: CustomFormatter()},
    },
    "handlers": {
        "customhandler": {
            "filters": ["user"],
            "formatter": "customformatter",
            "class": "logging.StreamHandler"
        }
    },
    "root": {
        "handlers": ["customhandler"],
        "level": "INFO",
        "propagate": False,
    },
    "loggers": {
        "uvicorn.access": {
            "handlers": ["customhandler"],
            "level": "INFO",
            "propagate": True
        },
        "uvicorn.error": {
            "handlers": ["customhandler"],
            "level": "INFO",
            "propagate": True
        }
    }
}

if __name__ == "__main__":
    import logging.config

    logging.config.dictConfig(logging_config)

    logger = logging.getLogger(__name__)

    logger.info("test")