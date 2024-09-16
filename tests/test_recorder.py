import unittest
import time

from crawler.recorder import Recorder
from crawler.utils import redis


def test_redis_connection():
    redis.set('test', 'test')
    rsp = redis.get('test')
    assert rsp == b'test'


class TestRecorder(unittest.TestCase):
    def setUp(self):
        time_hex = hex(int(time.time()))[2:]
        self.recorder = Recorder(time_hex)

    def test_register(self):
        task_id = "test_main_task_id"
        self.recorder.register_workflow_id(task_id)
        rsp = self.recorder.get_workflow_task_id()
        self.assertEqual(rsp, task_id)  # add assertion here

    def test_assert_visited_url(self):
        url = "test_url"
        rsp = self.recorder.assert_visited_url(url)
        self.assertFalse(rsp)
        self.recorder.record_visited_url(url)
        rsp = self.recorder.assert_visited_url(url)
        self.assertTrue(rsp)

    def test_record_task_id(self):
        task_id = ['task_id1', 'task_id2', 'task_id3']
        for tid in task_id:
            self.recorder.record_task_id(tid)
        rsp = self.recorder.get_all_task_id()
        self.assertEqual(task_id, rsp)


if __name__ == '__main__':
    unittest.main()
