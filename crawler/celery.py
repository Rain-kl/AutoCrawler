import celery
from config.settings import settings, celery_include
from celery.signals import task_postrun, task_failure

if settings.task_queue == 'redis':
    backend = settings.redis_url
    broker = settings.redis_url
else:
    backend = settings.rabbitmq_url
    broker = settings.rabbitmq_url

celery_app = celery.Celery(
    'tasks',
    broker=broker,
    backend=backend,
    include=celery_include
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    worker_hijack_root_logger=False,  # 避免Celery接管根logger
    result_expires=3600,  # 任务结果过期时间10分钟
)


# @task_prerun.connect
# def task_prerun_handler(sender=None, task_id=None, task=None, **kwargs):
#     print(f'Task {task.name} (ID: {task_id}) is about to start.')

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, **kwargs):
    print(f'Task {task.name} (ID: {task_id}) has finished.')


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    print(f'Task {sender.name} (ID: {task_id}) failed with exception: {exception}')
