# scripts/run_master.py

from workers.master_node import master_node

if __name__ == "__main__":
    # 添加示例任务
    master_node.add_task({"url": "http://example.com"})
    master_node.add_task({"url": "http://example.org"})

    print("Master node started, tasks added.")

    # 启动监控功能（可选）
    # master_node.monitor_workers()