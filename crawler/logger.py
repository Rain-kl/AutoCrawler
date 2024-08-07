# crawler/logger.py

from config.logging_config import logger


class Logger:
    @staticmethod
    def log_info(self, message):
        logger.info(message)

    @staticmethod
    def log_warning(self, message):
        logger.warning(message)

    @staticmethod
    def log_error(self, message):
        logger.error(message)

    @staticmethod
    def log_debug(self, message):
        logger.debug(message)


# 在项目中使用 Logger
logger_instance = Logger()
