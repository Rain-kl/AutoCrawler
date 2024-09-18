# crawler/workflow.py
import random
import threading
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from hashlib import md5
from config.logging_config import logger
from data.loader import DataLoader
from data.processor import DataProcessor, AutoProcessor
from .model import Param, ResponseModel
from .recorder import Recorder
from .utils import get_celery_result


class Workflow(ABC):
    def __init__(
            self,
            *,
            domain: str,
            start_path: str,
            end_path_regex: str,
            data_loader: DataLoader
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
        self.data_loader: DataLoader = data_loader
        self.executor = ThreadPoolExecutor(max_workers=10)  # Adjust max_workers as necessary
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
            # 等待获取workflow的task_id, 这个task_id是主任务的task_id
            stop_flag = recorder.get_stop_flag()
            if stop_flag is not None:
                break

        logger.info("workflow stopped")
        self.stop_event.set()  # Signal threads to stop

    @abstractmethod
    def main(self):
        raise NotImplementedError("main method should be implemented in subclass")

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
                self.executor.submit(self.task_pipeline, task_id_set)
        self.executor.shutdown(wait=True)  # Wait for threads to finish

    def task_pipeline(self, task_id_set: list):
        result_data_list = []
        for task_id in task_id_set:
            result_data = get_celery_result(task_id)
            processed_data = self.data_processing(
                ResponseModel.model_validate(result_data)
            )
            result_data_list.append(processed_data)

        self.data_loader.load(result_data_list)
        data_processor = AutoProcessor(self.data_loader)
        self.data_storage(data_processor, result_data_list)

    @abstractmethod
    def data_storage(self, data_processor: DataProcessor, data: [ResponseModel]):
        raise NotImplementedError("data_storage method should be implemented in subclass")

    def data_processing(self, data: ResponseModel) -> ResponseModel:
        print(data)
        return data
