# crawler/workflow.py
import random
import threading
import time
from hashlib import md5

from config.logging_config import logger
from .model import Param
from .recorder import Recorder
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
        self.wait_flag = 0
        print(f"Workflow ID: {self.param_base.workflow_id}")

    def start(self):
        """
        启动工作流
        :return:
        """
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
        task_id_set = recorder.get_all_task_id()
        for task_id in task_id_set:
            self.task_pipline(task_id)

    def wait_result(self):
        """
        等待任务
        :return:
        """
        recorder = Recorder(self.param_base.workflow_id)
        while not self.stop_event.is_set():
            time.sleep(1)
            task_id_set = recorder.get_updated_task_id()
            if task_id_set:
                print(f"task_id: {task_id_set}\nlen: {len(task_id_set)}")

    def main(self):
        raise NotImplementedError("main method should be implemented in subclass")

    def task_pipline(self, task_id):
        return self.data_processing(get_celery_result(task_id))

    def data_processing(self, data):
        print(data)
        return data
