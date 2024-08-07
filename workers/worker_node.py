# workers/worker_node.py

import json
import redis
import time
from logging import getLogger
from crawler.requester import requester
from crawler.parser import parser
from crawler.data_processor import data_processor
from crawler.storage import mongo_storage

logger = getLogger("crawler.worker_node")


class WorkerNode:
    def __init__(self):
        self.redis_client = redis.StrictRedis.from_url(settings.redis_url)
        self.task_queue_key = "task_queue"
        self.result_queue_key = "result_queue"

    def get_task(self):
        task = self.redis_client.blpop(self.task_queue_key, timeout=5)
        if task:
            return json.loads(task[1])
        return None

    def process_task(self, task):
        url = task.get('url')
        if url:
            response = requester.send_request(url)
            if response:
                soup = parser.parse_html(response.content)
                data = data_processor.extract_information(soup)
                self.send_result(data)
                return data
            else:
                logger.error(f"Failed to fetch {url}")
        return None

    def send_result(self, result):
        result_json = json.dumps(result)
        self.redis_client.rpush(self.result_queue_key, result_json)
        logger.info(f"Sent result to queue: {result}")

    def start_worker(self):
        while True:
            task = self.get_task()
            if task:
                self.process_task(task)
            time.sleep(1)  # 避免无限循环占用CPU


# 实例化从节点
worker_node = WorkerNode()