#!/usr/bin/env python

import os
import subprocess
import threading

from loguru import logger
from dotenv import load_dotenv
from rich import print
from rich.panel import Panel
from rich.table import Table
import itertools

load_dotenv()

flower_port = os.getenv('FLOWER_PORT')
flower_address = os.getenv('FLOWER_ADDRESS')


def print_info():
    table = Table(title="", box=None, width=61)
    styles = itertools.cycle(
        ["#7CD9FF", "#BDADFF", "#9EFFE3", "#f1b8e4", "#F5A88E", "#BBCA89"]
    )
    metric = {
        "flower url": {
            'value': f"http://{flower_address}:{flower_port}",
        },
        "Task Queue": {
            'value': os.getenv('TASK_QUEUE'),
        },
        "Celery Include": {
            'value': os.getenv('CELERY_INCLUDE'),
        },
        "Redis URL": {
            'value': os.getenv('REDIS_URL'),
        },
    }
    table.add_column("", justify='left', width=12)
    table.add_column("", justify='left')
    for key, value in metric.items():
        if value['value']:
            table.add_row(key, value['value'], style=next(styles))

    print(
        Panel(
            table,
            title=f"🤗 celery worker is ready! ",
            expand=False,
        )
    )


def start_celery_worker_and_flower(workdir, celery_module):
    os.chdir(workdir)

    worker_cmd = ['celery', '-A', celery_module, 'worker', '--loglevel=info']
    flower_cmd = ['celery', '-A', celery_module, 'flower', f'--port={flower_port}',
                  f'--address={flower_address}']

    worker_process = subprocess.Popen(worker_cmd)
    flower_process = subprocess.Popen(flower_cmd)

    return worker_process, flower_process


def cleanup(worker_process, flower_process):
    print("Stopping Celery Worker and Flower...")
    exit(0)
    # worker_process.terminate()
    # flower_process.terminate()
    # worker_process.wait()
    # flower_process.wait()


def main():
    workdir = './'
    celery_module = "crawler"

    worker_process, flower_process = start_celery_worker_and_flower(workdir, celery_module)

    # def signal_handler(sig, frame):
    #     cleanup(worker_process, flower_process)
    #     sys.exit(0)
    #
    # signal.signal(signal.SIGINT, signal_handler)

    # Wait for the subprocesses to complete
    worker_process.wait()
    flower_process.wait()


if __name__ == "__main__":
    # 获取当前执行路径
    cwd = (os.getcwd())
    if 'script' in cwd:
        logger.error('current path is script, change to parent path')
    else:
        print_info()
        thread = threading.Thread(target=main)
        thread.start()
        thread.join()
