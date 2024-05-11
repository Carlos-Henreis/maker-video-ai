import os
import logging
import logging.config


class LoggingConfig:

    def __init__(self):
        self._setup_logging()
        self._LOGGER = logging.getLogger(__name__)


    def _setup_logging(self):
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        logging.basicConfig(level=log_level)

    def get_logger(self):
        return self._LOGGER