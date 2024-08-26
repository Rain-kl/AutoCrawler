# 解释重要model与名词

- workflow_id: 任务流被初始化时根据时间戳与随机数哈希生成的唯一标识， 用于标识任务流。
其定义在Recorder类中。通过workflow_id可以取出任务流的所有信息，包括task_id
- taskid：是celery返回的任务uuid，通过task_id可以取出任务结果

## 流程与指南
参考workflow_example.py，继承Workflow类，实现``main``方法
    
Workflow需要主域名和路径，实例化时根据此信息生成workflow_id，所以在实现main方法时，需要使用``@register_crawler``修饰器用于注册爬虫，目的告诉``wait_result``何时结束

运行起工作流时需要用Workflow的```start```方法，同时启动``main``和``wait_result``方法，``wait_result``用于等待任务流结束

当任务流结束后，会获取所有的taskid送往`task_pipline`转变为任务结果再传递给`data_process`处理,使用``data_process``可以将数据传递给``data``库进行操作