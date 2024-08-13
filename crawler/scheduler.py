# crawler/scheduler.py

import time
import threading
from queue import Queue

from .workflow import MyWorkflow


class Scheduler(MyWorkflow):
    def __init__(
            self,
            domain: str,
            start_path="/book/166492/",
            end_path_regex="/book/166492/.*html"
    ):
        super().__init__(domain, start_path, end_path_regex)
        self.task_queue = Queue()
        self.jobs = []
        self.is_running = False

    def start(self):
        self.main()

    def commit_async_task(self, tag, task: [callable]):
        pass


    def data_offload(self, tag, target):
        pass

    def pull_task_response(self):
        pass

    def stop(self):
        self.is_running = False

    def run(self):
        while self.is_running:
            if not self.task_queue.empty():
                task = self.task_queue.get()  # 获取任务
                if task:
                    task()  # 执行任务
                    self.task_queue.task_done()  # 任务完成, 从队列中移除
            time.sleep(1)  # 间隔

    def add_task(self, task):
        self.task_queue.put(task)

    def add_job(self, func, interval):
        job = threading.Thread(target=self.schedule_task, args=(func, interval))
        job.start()
        self.jobs.append(job)

    def schedule_task(self, func, interval):
        while self.is_running:
            func()
            time.sleep(interval)  # 间隔
