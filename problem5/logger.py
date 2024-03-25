import logging


LOG_PATH = "logs"

def create_logger():
    logger = logging.getLogger(__name__)
    return logger

# logging.handlers.RotatingFileHandler()

LOGGER = create_logger()
