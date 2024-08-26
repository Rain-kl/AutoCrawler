# crawler/recorder.py
import json

import celery.result

from config.logging_config import logger
from .decorator import cache


class Recorder:
    """
    workflow_id: 当workflow实例化时生成的唯一id
    cache_visited_id: cache数据库的key, 用于记录已访问的url，存储方式为visited-{workflow_id}: set[url,...]
    cache_task_id: cache数据库的key, 用于记录task_id，存储方式为task-{workflow_id}: set[task_id,...]
    """

    def __init__(self, workflow_id):
        self.workflow_id = workflow_id
        self.cache_visited_id = f"visited-{self.workflow_id}"
        self.cache_task_id = f"task-{self.workflow_id}"
        self.cache_queue: set = set()

    def register_workflow_id(self, task_id):
        """
        注册workflow_id, 用于记录任务状态(完成失败等)
        :param task_id:
        :return:
        """
        if isinstance(task_id, str):
            cache.set(self.workflow_id, task_id)
        else:
            raise ValueError("task_id should be str")

    def get_workflow_task_id(self):
        """
        获取workflow_id对应的task_id，用于查询主任务状态
        :return:
        """
        result = cache.get(self.workflow_id)
        if isinstance(result, celery.result.AsyncResult):
            logger.warning(f"task_id: {result.id} should be str")
            return result.id
        return result

    def record_visited_url(self, url):
        """
        记录已访问的url
        :param url:
        :return:
        """
        result = cache.get(self.cache_visited_id)
        if result is None:
            url_set = [url]
            cache.set(self.cache_visited_id, url_set)
        else:
            result.append(url)
            cache.set(self.cache_visited_id, result)

    def assert_visited_url(self, url):
        """
        判断url是否已经访问过
        :param url:
        :return:
        """
        result = cache.get(self.cache_visited_id)
        if result is None:
            return False
        return url in result

    def record_task_id(self, task_id) -> list:
        """
        记录task_id
        :param task_id:
        :return:
        """
        print(f"#debug# task_id: {task_id}")
        if not isinstance(task_id, str):
            raise ValueError("task_id should be str")
        task_id_set: list = cache.get(self.cache_task_id)
        if task_id_set is None:
            task_id_set = list()
            task_id_set.append(task_id)
            cache.set(self.cache_task_id, task_id_set)
        else:
            if task_id in task_id_set:
                raise ValueError(f"task_id: {task_id} already exists")
            task_id_set.append(task_id)
            cache.set(self.cache_task_id, task_id_set)
        print(f"#debug# task_id_set: {task_id_set}")
        return task_id_set

    def empty_task_id(self) -> None:
        cache.set(self.cache_task_id, None)

    def get_all_task_id(self) -> list:
        """
        获取所有task_id
        :return:
        """
        return cache.get(self.cache_task_id)

    def get_updated_task_id(self)->set:
        """
        每一次调会获取全部task_id, 并与上一次的task_id做差集，返回差集，为新增的task_id
        :return:
        """
        all_task_id = self.get_all_task_id()
        if all_task_id is None:
            return set()
        difference = self.cache_queue.symmetric_difference(set(all_task_id))
        self.cache_queue = set(all_task_id).copy()
        return difference


def register_crawler(func):
    def wrapper(self, *args, **kwargs):
        recorder = Recorder(self.param_base.workflow_id)
        task_obj = func(self, *args, **kwargs)
        recorder.register_workflow_id(task_obj.id)
        return task_obj

    return wrapper
