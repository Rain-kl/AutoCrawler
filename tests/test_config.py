# 在任意模块中使用配置
from config.settings import settings
from config.logging_config import logger


def test_config():
    print('\n\n------------------------------')
    print(settings)
    print('------------------------------')

    assert isinstance(settings.task_queue, str)

def test_logger():
    logger.info('info message')
    logger.error('error message')
    logger.debug('debug message')
    logger.warning('warning message')
    logger.critical('critical message')
    assert True