# crawler/workflow_example.py
import celery.result

from config.logging_config import logger
from data.loader import DataLoader, TextLoader
from data.processor import TextProcessor
from .celery import celery_app
from .model import Param, ResponseModel
from .recorder import Recorder
from .recorder import register_crawler
# from celery.utils.log import get_task_logger
from .workflow import Workflow


class WorkflowExample(Workflow):
    def __init__(self, domain: str, start_path: str, end_path_regex: str):
        super().__init__(domain, start_path, end_path_regex)

    @register_crawler
    def main(self) -> celery.result.AsyncResult:
        print(f"Start crawling from: {self.domain + self.start_path}")
        param = self.param_base.model_copy(
            update={
                'tag': 'chapter',
                'url_path': self.start_path
            }
        )
        return step1.delay(param)

    def data_processing(self, data) -> ResponseModel:
        print(data)
        return data

    def data_loader(self) -> DataLoader:
        return TextLoader()

    def data_storage(self, data_processor: TextProcessor, data: [ResponseModel]):
        data_processor.save_txt("save.txt")


@celery_app.task(bind=True, max_retries=3, default_retry_delay=3)
def step1(self, params: Param):
    """
    提交任务，返回结果，任务全部提交完成
    """
    try:
        if isinstance(params, dict):
            params = Param(**params)
        recorder = Recorder(params.workflow_id)
        logger.info(f"Start crawling from: {params.url}")
        ...
        step2.delay(params)
        recorder.record_visited_url(params.url)
        ...
        return ResponseModel(tag=params.workflow_id, response='success')
    except Exception as exc:
        self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=3)
def step2(self, params: Param) -> ResponseModel:
    """
    执行完成，返回任务结果
    """
    try:
        if isinstance(params, dict):
            params = Param(**params)
        logger.info(f"Start crawling from: {params.url}")
        ...
        return ResponseModel(tag=params.tag, response='context')
    except Exception as exc:
        self.retry(exc=exc)
