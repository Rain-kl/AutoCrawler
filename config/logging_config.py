import datetime
from loguru import logger


# 函数生成文件名
def get_log_file_path(level):
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))  # 获取当前时间, 并设置时区为东八区
    return './logs/' + f'{level}-{now.strftime("%Y-%m-%d")}.log'


# 配置每个日志级别的文件
logger.add(get_log_file_path("success"),
           filter=lambda record: record["level"].name == "SUCCESS", level="SUCCESS", rotation="00:00")
logger.add(get_log_file_path("info"),
           filter=lambda record: record["level"].name == "INFO", level="INFO", rotation="00:00")
logger.add(get_log_file_path("debug"),
           filter=lambda record: record["level"].name == "DEBUG", level="DEBUG", rotation="00:00")
logger.add(get_log_file_path("error"),
           filter=lambda record: record["level"].name == "ERROR", level="ERROR", rotation="00:00")
