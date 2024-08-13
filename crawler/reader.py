# from .celery import celery_app
from .decorator import cache
from celery.result import AsyncResult


def record_task_id(workflow_id, task_id):
    if not workflow_id.startswith('reader-'):
        workflow_id=f"reader-{workflow_id}"
    result = cache.get(workflow_id)
    if result is None:
        task_id_set = [task_id]
        cache.set(workflow_id, task_id_set)
    else:
        result.append(task_id)
        cache.set(workflow_id, result)


def empty_task_id(workflow_id):
    if not workflow_id.startswith('reader-'):
        workflow_id=f"reader-{workflow_id}"
    cache.set(workflow_id, None)


def get_task_id(workflow_id):
    if not workflow_id.startswith('reader-'):
        workflow_id=f"reader-{workflow_id}"
    return cache.get(workflow_id)


def get_realdata(task_id):
    result = AsyncResult(task_id)
    return result.get()

def save_text(workflow_id:str):
    if not workflow_id.startswith('reader-'):
        workflow_id=f"reader-{workflow_id}"
    tasks_id = get_task_id(workflow_id)
    if tasks_id is None:
        raise ValueError(f"no tasks found for {workflow_id}")
    print(f"read {len(tasks_id)} tasks")
    with open(f'{workflow_id}.txt', 'w') as f:
        for task_id in tasks_id:
            print(task_id)
            result = get_realdata(task_id.id)
            print(result)
            content=f"\n# {result['tag']}\n{result['response']}\n"
            f.write(content)
    empty_task_id(workflow_id)




