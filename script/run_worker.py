# scripts/run_worker.py

from workers.worker_node import worker_node

if __name__ == "__main__":
    print("Worker node started.")
    worker_node.start_worker()