# workers/master_node.py

import json
import redis
from config.settings import settings
from logging import getLogger

logger = getLogger("crawler.master_node")

class MasterNode:
    def __init__(self):
        self.redis_client = redis.StrictRedis.from_url(settings.redis_url)
        self.task_queue_key = "task_queue"

    def add_task(self, task):
        task_json = json.dumps(task)
        self.redis_client.rpush(self.task_queue_key, task_json)
        logger.info(f"Added task to queue: {task}")

    def monitor_workers(self):
        # 监控和协调工作节点的状态和任务完成情况
        pass

    def collect_results(self):
        # 收集各个工作节点的爬取结果
        pass

# 实例化主节点
master_node = MasterNode()