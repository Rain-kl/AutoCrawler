import logging
from logging.config import dictConfig
import os
from .settings import settings
from .colored_formatter import ColoredFormatter  # 导入自定义的彩色格式化器

# 确保日志目录存在，否则创建该目录
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - [%(levelname)s] - %(name)s - %(module)s:%(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": settings.log_level,
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file_debug": {
            "level": "DEBUG",
            "formatter": "detailed",
            "class": "logging.FileHandler",
            "filename": os.path.join(log_directory, "crawler_debug.log"),
            "mode": "a",
        },
        "file_info": {
            "level": "INFO",
            "formatter": "detailed",
            "class": "logging.FileHandler",
            "filename": os.path.join(log_directory, "crawler_info.log"),
            "mode": "a",
        },
        "file_error": {
            "level": "ERROR",
            "formatter": "detailed",
            "class": "logging.FileHandler",
            "filename": os.path.join(log_directory, "crawler_error.log"),
            "mode": "a",
        }
    },
    "root": {
        "level": settings.log_level,
        "handlers": ["console", "file_debug", "file_info", "file_error"]
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False
        },
        "crawler": {
            "level": settings.log_level,
            "handlers": ["console", "file_debug", "file_info", "file_error"],
            "propagate": False,
        }
    },
}

# 配置日志
dictConfig(log_config)
logging.getLogger("httpx").setLevel(logging.WARNING)  # 设置 httpx 的日志级别为 WARNING
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("chardet").setLevel(logging.WARNING)

# 获取控制台处理程序并应用自定义的彩色格式化器
console_handler = logging.getLogger().handlers[0]
console_handler.setFormatter(ColoredFormatter("%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"))

logger = logging.getLogger("crawler")