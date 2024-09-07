#!/usr/bin/env bash

workdir='./'
echo "workdir: ${workdir}"
celery_module="crawler"

cd ${workdir}

# 启动 Celery Worker 和 Flower
celery -A ${celery_module} worker --loglevel=info & worker_pid=$!
celery -A ${celery_module} flower --port=5555 & flower_pid=$!

# 定义清理函数
cleanup() {
    echo "Stopping Celery Worker and Flower..."
    kill -TERM $worker_pid
    kill -TERM $flower_pid
    wait $worker_pid
    wait $flower_pid
}

# 捕获 SIGINT (Ctrl+C) 信号，并执行清理函数
trap cleanup SIGINT

# 等待后台进程
wait $worker_pid
wait $flower_pid