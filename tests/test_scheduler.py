# tests/test_scheduler.py

import pytest
from crawler.scheduler import Scheduler


def test_scheduler_add_task():
    scheduler = Scheduler()
    task_executed = False

    def dummy_task():
        nonlocal task_executed
        task_executed = True

    scheduler.add_task(dummy_task)
    scheduler.start()
    scheduler.stop()

    assert task_executed


def test_scheduler_run():
    scheduler = Scheduler()
    dummy_task_executed = []

    def dummy_task():
        dummy_task_executed.append(True)

    scheduler.add_task(dummy_task)
    scheduler.start()
    assert not scheduler.task_queue.empty()
    scheduler.stop()