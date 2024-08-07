# config/settings.py
from typing import Union

from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # HTTP 请求相关配置
    request_timeout: int = 10  # 请求超时时间（秒）

    # 数据库相关配置
    mongodb_url: AnyUrl = "mongodb://localhost:27017/my_database"
    postgres_url: AnyUrl = "postgresql://user:password@localhost:5432/my_database"

    # Redis 相关配置（用于任务队列）
    redis_url: AnyUrl = "redis://localhost:6379/0"

    # 日志相关配置
    log_level: str = "INFO"

    proxy_host: str|None = None
    proxy_port: Union[str, int, list,None] = None

    # 可以从配置文件加载配置
    class Config:
        env_file = ".env"


# 实例化全局配置对象
settings = Settings()
