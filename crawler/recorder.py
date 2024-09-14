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
        result = redis.get(self.cache_visited_id)
        if result is None:
            url_set = [url]
            url_set_s = json.dumps(url_set)
            redis.set(self.cache_visited_id, url_set_s)
        else:
            if isinstance(result, bytes):
                result = result.decode()
            json_data: list = json.loads(result)
            json_data.append(url)
            result = json.dumps(json_data)
            redis.set(self.cache_visited_id, result)

    def assert_visited_url(self, url):
        """
        判断url是否已经访问过
        :param url:
        :return:
        """
        result = redis.get(self.cache_visited_id)
        if result is None:
            return False
        if isinstance(result, bytes):
            result = result.decode()
        json_data: list = json.loads(result)
        return url in json_data

    def record_task_id(self, task_id: str) -> list:
        """
        记录task_id
        :param task_id:
        :return:
        """
        print(f"#debug# task_id: {task_id}")
        if not isinstance(task_id, str):
            raise ValueError("task_id should be str")
        task_id_set_b: Union[bytes, str] = redis.get(self.cache_task_id)
        if task_id_set_b is None:
            task_id_set = list()
            task_id_set.append(task_id)
            task_id_set_s = json.dumps(task_id_set)
            redis.set(self.cache_task_id, task_id_set_s)
        else:
            if isinstance(task_id_set_b, bytes):
                task_id_set_b = task_id_set_b.decode()
            task_id_set = json.loads(task_id_set_b)
            if task_id in task_id_set:
                raise ValueError(f"task_id: {task_id} already exists")
            task_id_set.append(task_id)
            task_id_set_s = json.dumps(task_id_set)
            cache.set(self.cache_task_id, task_id_set_s)
        print(f"#debug# task_id_set: {task_id_set_s}")
        return task_id_set

    def empty_task_id(self) -> None:
        redis.set(self.cache_task_id, None)

    def get_all_task_id(self) -> Union[bytes, str]:
        """
        获取所有task_id
        :return:
        """
        rsp = redis.get(self.cache_task_id)
        if isinstance(self.cache_task_id, bytes):
            rsp = rsp.decode()
        task_id_set = json.loads(rsp)
        return task_id_set

    def get_updated_task_id(self) -> set:
        """
        每一次调会获取全部task_id, 并与上一次的task_id做差集，返回差集，为新增的task_id
        :return:
        """
        all_task_id = self.get_all_task_id()
        if all_task_id is None:
            return set()
        all_task_id = json.loads(all_task_id)
        difference = self.cache_queue.symmetric_difference(set(all_task_id))
        self.cache_queue = set(all_task_id).copy()
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
