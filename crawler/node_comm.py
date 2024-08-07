# crawler/node_comm.py

import json
import redis
from config.settings import settings

class NodeCommunicator:
    def __init__(self):
        self.redis_client = redis.StrictRedis.from_url(settings.redis_url)

    def send_task(self, task):
        self.redis_client.rpush('task_queue', json.dumps(task))

    def receive_task(self):
        task = self.redis_client.blpop('task_queue', timeout=5)
        if task:
            return json.loads(task[1])
        return None

# 在项目中使用 NodeCommunicator
node_comm = NodeCommunicator()