# crawler/scheduler.py

import time
import threading
from queue import Queue

class Scheduler:
    def __init__(self):
        self.task_queue = Queue()
        self.jobs = []
        self.is_running = False

    def start(self):
        self.is_running = True
        threading.Thread(target=self.run).start()

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

# 在项目中使用 Scheduler
scheduler = Scheduler()