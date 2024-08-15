# crawler/workflow.py
import random
import threading
import time
from hashlib import md5

import celery.result
from config.logging_config import logger
from .model import Param
from .decorator import cache
from .utils import get_celery_result


class Workflow:
    def __init__(
            self,
            domain: str,
            start_path: str,
            end_path_regex: str,
            # work_type="text",
    ):
        self.stop_event = threading.Event()  # 用于停止线程
        self.domain = domain.rstrip('/')
        self.start_path = '/' + start_path.strip('/')
        self.end_path_regex = end_path_regex
        workflow_id = md5(
            (
                    str(time.time())
                    + str(random.randint(0, 100000))
            ).encode()).hexdigest()[0:16]
        self.param_base = Param(
            workflow_id=workflow_id,
            domain=domain,
            url_path=start_path,
            end_path_regex=end_path_regex,
            url_params={
                "param": None,
                "data": None,
                "json": None,
            }
        )
        print(f"Workflow ID: {self.param_base.workflow_id}")

    def start(self):
        thread_main = threading.Thread(target=self.main)
        thread_wait = threading.Thread(target=self.wait_result)
        thread_main.start()
        thread_wait.start()
        recorder = Recorder(self.param_base.workflow_id)
        while True:
            time.sleep(2)
            task_id = recorder.get_workflow_task_id()
            if task_id is not None:
                break

        logger.info(get_celery_result(task_id))

        time.sleep(1)
        self.stop_event.set()  # Signal threads to stop

    def wait_result(self):
        recorder = Recorder(self.param_base.workflow_id)
        while not self.stop_event.is_set():
            time.sleep(1)
            task_id = recorder.get_task_id()
            print(f"\ntask_id: {task_id}\nlen: {len(task_id)}\n")

    def main(self):
        raise NotImplementedError("main method should be implemented in subclass")


class Recorder:
    def __init__(self, workflow_id):
        self.workflow_id = workflow_id
        self.visited_id = f"visited-{self.workflow_id}"
        self.cache_task_id = f"task-{self.workflow_id}"
        self.cache_queue: set = set()

    def register_workflow_id(self, task_id):
        """
        注册workflow_id, 用于记录任务状态(完成失败等)
        :param task_id:
        :return:
        """
        cache.set(self.workflow_id, task_id)

    def get_workflow_task_id(self):
        """
        获取workflow_id对应的task_id
        :return:
        """
        result = cache.get(self.workflow_id)
        if isinstance(result, celery.result.AsyncResult):
            return result.id
        return result

    def record_visited_url(self, url):
        """
        记录已访问的url
        :param url:
        :return:
        """
        result = cache.get(self.visited_id)
        if result is None:
            url_set = [url]
            cache.set(self.visited_id, url_set)
        else:
            result.append(url)
            cache.set(self.visited_id, result)

    def assert_visited_url(self, url):
        """
        判断url是否已经访问过
        :param url:
        :return:
        """
        result = cache.get(self.visited_id)
        if result is None:
            return False
        return url in result

    def record_task_id(self, task_id) -> set:
        """
        记录task_id
        :param task_id:
        :return:
        """
        task_id_set: set = cache.get(self.cache_task_id)
        if task_id_set is None:
            task_id_set = set()
            task_id_set.add(task_id)
            cache.set(self.cache_task_id, task_id_set)
        else:
            task_id_set.add(task_id)
            cache.set(self.cache_task_id, task_id_set)
        return task_id_set

    def empty_task_id(self):
        cache.set(self.cache_task_id, None)

    def get_all_task_id(self):
        """
        获取所有task_id
        :return:
        """
        return cache.get(self.cache_task_id)

    def get_task_id(self):
        """
        获取新的task_id
        :return:
        """
        all_task_id = self.get_all_task_id()
        if all_task_id is None:
            return set()
        difference = self.cache_queue.symmetric_difference(all_task_id)
        self.cache_queue = all_task_id.copy()
        return difference


def register_crawler(func):
    def wrapper(self, *args, **kwargs):
        recorder = Recorder(self.param_base.workflow_id)
        task_id = func(self, *args, **kwargs)
        recorder.register_workflow_id(task_id)
        return task_id

    return wrapper
