import getpass
import logging

class NoBadWordsFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:
        setattr(record, "user", getpass.getuser())
        return True

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addFilter(NoBadWordsFilter())

logger.info("working")
logger.info("F")