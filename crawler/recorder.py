# crawler/recorder.py
import json
from typing import Union

from config.logging_config import logger
from .decorator import cache
from .utils import redis


class Recorder:
    """
    workflow_id: 当workflow实例化时生成的唯一id
    cache_visited_id: cache数据库的key, 用于记录已访问的url，存储方式为visited-{workflow_id}: set[url,...]
    cache_task_id: cache数据库的key, 用于记录task_id，存储方式为task-{workflow_id}: set[task_id,...]
    """

    def __init__(self, workflow_id):
        self.workflow_id: str = workflow_id
        self.cache_visited_id: str = f"visited-{self.workflow_id}"
        self.cache_task_id: str = f"task-{self.workflow_id}"
        self.cache_queue: set = set()

    def register_workflow_id(self, task_id):
        """
        注册workflow_id, 用于记录任务状态(完成失败等)
        :param task_id:
        :return:
        """
        if isinstance(task_id, str):
            redis.set(self.workflow_id, task_id)
        else:
            raise ValueError("task_id should be str")

    def get_workflow_task_id(self) -> str:
        """
        获取workflow_id对应的task_id，用于查询主任务状态
        :return:
        """
        result = redis.get(self.workflow_id)
        if isinstance(result, bytes):
            result = result.decode()
        return result

    def record_visited_url(self, url):
        """
        记录已访问的url
        :param url:
        :return:
        """
        redis.sadd(self.cache_visited_id, url)

    def assert_visited_url(self, url):
        """
        判断url是否已经访问过
        :param url:
        :return:
        """
        return redis.sismember(self.cache_visited_id, url)

    def record_task_id(self, task_id: str) -> None:
        """
        记录task_id
        :param task_id:
        :return:
        """
        print(f"#debug# task_id: {task_id}")
        if not isinstance(task_id, str):
            raise ValueError("task_id should be str")

        task_id_list = redis.lrange(self.cache_task_id, 0, -1)
        task_id_list = [item.decode() if isinstance(item, bytes) else item for item in task_id_list]

        if task_id in task_id_list:
            raise ValueError(f"task_id: {task_id} already exists")

        redis.rpush(self.cache_task_id, task_id)
        task_id_list.append(task_id)

    def get_all_task_id(self) -> list:
        """
        获取所有task_id
        :return:
        """
        task_id_list = redis.lrange(self.cache_task_id, 0, -1)
        task_id_list = [item.decode() if isinstance(item, bytes) else item for item in task_id_list]
        return task_id_list

    def get_updated_task_id(self) -> set:
        """
        每一次调会获取全部task_id, 并与上一次的task_id做差集，返回差集，为新增的task_id
        :return:
        """
        all_task_id = self.get_all_task_id()
        difference = set(all_task_id).difference(self.cache_queue)
        self.cache_queue = all_task_id.copy()
        return difference

    def empty_all(self):
        redis.delete(self.cache_visited_id)
        redis.delete(self.cache_task_id)
        redis.delete(self.workflow_id)


def register_crawler(func):
    def wrapper(self, *args, **kwargs):
        recorder = Recorder(self.param_base.workflow_id)
        task_obj = func(self, *args, **kwargs)
        recorder.register_workflow_id(task_obj.id)  # 注册workflow_id, 当注册之后，便通过该id查询任务结果
        logger.success(f"Register workflow_id: {self.param_base.workflow_id}")
        return task_obj

    return wrapper
