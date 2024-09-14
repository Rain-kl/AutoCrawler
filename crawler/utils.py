from celery.result import AsyncResult
from config.settings import settings
from .celery import celery_app
from redis import Redis


def get_redis() -> Redis:
    """
    初始化Redis
    :return:
    """
    redis_host = settings.redis_url.split("://")[1].split(":")[0]
    redis_port = settings.redis_url.split(":")[2].split("/")[0]
    redis_db = settings.redis_url.split("/")[-1]
    return Redis(host=redis_host, port=redis_port, db=redis_db)


redis = get_redis()


def get_celery_result(task_id) -> dict:
    """
    【阻塞】获取Celery任务结果
    :param task_id:
    :return:
    """
    result = AsyncResult(id=task_id, app=celery_app)
    while True:
        if result.successful():
            return result.get()
        elif result.failed():
            return result.traceback


def parse_url(domain: str, url: str) -> str:
    if url.startswith('http'):
        return url
    return domain + url
