from celery.result import AsyncResult
from .celery import celery_app


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


if __name__ == '__main__':
    get_celery_result('fc561de3-459d-4a70-a1b5-cd5e4b9a9975')
