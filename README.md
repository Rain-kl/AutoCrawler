# AutoCrawler

AutoCrawler 是一个 Apache2 许可的分布式的快速高级网络爬虫和网页抓取框架，可以通过大语言模型快速聚焦网页主题，抓取数据内容。

当前项目正处于开发阶段，以下介绍是基于项目的预期功能,并不代表已经实现的功能。

---

## 目录

* [预计功能](README.md#预计功能)
* [工作流程](README.md#工作流程)
* [项目架构](README.md#项目架构)
* [解决的痛点](README.md#解决的痛点)
* [快速上手](README.md#快速上手)
    * [1. 环境配置](README.md#1-环境配置)
    * [2. 工作流开发](README.md#2-工作流开发)
    * [3. 初始化配置文件](README.md#3-初始化配置文件)
    * [4. 一键启动](README.md#4-一键启动)
* [项目进度](README.md#项目进度)


## 预计功能

🤖️ AutoCrawler提供各种实用的工具，例如通过大语言模型提取网页url或text

💡 当工作流编写完毕后可以投入调度器运行，调度器采用分布式框架celery。当工作流提交后，celery节点会自动获取任务并执行。

✅ 本项目还会提供网页端进行管理任务分配，任务监控，任务日志查看等功能。

📊 项目提供多种数据存储方式，包括数据库存储，文件存储，ES存储等。

## 工作流程
用户提交工作流后，scheduler会启动这个工作流，同时开启一个线程等待工作流的完成。
当工作流完成后，等待线程会将工作流的结果通过管道传递给调度器，调度器会将结果存储到数据处理模块中。
管道中存在可被用户定义的数据处理模块，用户可以通过继承`Workflow`类，实现`data_processing`方法，对数据进行处理。或者集成大语言模型以一定的规则处理这些数据

调度器提供接口由前端调用，前端可以通过接口查看任务的状态，任务的日志，任务的结果等。

## 项目架构
```shell
my_spider_project/
├── api/
│   ├── __init__.py
│   ├── endpoints.py               # 定义API端点，包含运行时信息等
├── config/
│   ├── __init__.py
│   ├── settings.py                # 全局配置文件
│   ├── logging_config.py          # 日志配置
├── crawler/
│   ├── __init__.py
│   ├── scheduler.py               # 调度模块
│   ├── requester.py               # 请求模块
│   ├── parser.py                  # 解析模块
│   ├── workflow.py                # 用户工作流引擎
│   │── workflow_example.py        # 工作流示例
│   │── recorder.py                # 工作流记录器
├── data/
│   ├── __init__.py
│   ├── data_processor.py          # 数据处理
│   ├── storage.py                 # 数据存储模块
├── plugins/                       # 插件目录，用于日后扩展
│   ├── __init__.py
│   ├── text_extractor.py          # 文本提取插件
│   ├── img_extractor.py           # 图片提取插件（未来扩展）
│   ├── video_extractor.py         # 视频提取插件（未来扩展）
├── workers/                       # 分布式节点管理
│   ├── __init__.py
│   ├── master_node.py             # 主节点模块
│   ├── worker_node.py             # 从节点模块
├── tests/                         # 测试目录
│   ├── __init__.py
│   ├── test_api.py                # API模块测试
│   ├── test_scheduler.py          # 调度模块测试
│   ├── test_requester.py          # 请求模块测试
│   ├── test_parser.py             # 解析模块测试
│   ├── test_data_processor.py     # 数据处理模块测试
│   ├── test_storage.py            # 数据存储模块测试
├── scripts/                       # 脚本目录，用于存放启动脚本和工具
│   ├── run_master.py              # 启动主节点脚本
│   ├── run_worker.py              # 启动从节点脚本
│   ├── run_api.py                 # 启动API服务脚本
├── static/                        # 静态资源目录（如配置文件或测试数据）
│   ├── sample_config.yaml         # 示例配置文件
│   ├── sample_data.json           # 示例数据
├── Dockerfile                     # Docker配置文件
├── docker-compose.yml             # Docker Compose文件
├── requirements.txt               # Python依赖包文件
├── README.md                      # 项目说明文档
```

## 解决的痛点

- 网页元素定位麻烦，且一个爬虫只能针对一个网站，可以通过自然语言的方式快速抓取网页内容
- 并发爬虫数据处理麻烦，本项目提供分布式框架celery，可以快速部署爬虫任务，并且有统一的数据处理方式
- 开发不同爬虫需要重复开发，本项目提供了一套通用的爬虫框架，可以快速开发不同的爬虫任务

## 快速上手

### 1. 环境配置

+ 首先，确保你的机器安装了 Python 3.8 - 3.11 (我们强烈推荐使用 Python3.11)。

```
$ python --version
Python 3.11.7
```

接着，创建一个虚拟环境，并在虚拟环境内安装项目的依赖

```shell

# 拉取仓库
$ git clone https://github.com/Rain-kl/AutoCrawler.git

# 进入目录
$ cd AutoCrawler

# 安装全部依赖
$ pip install -r requirements.txt 

```


### 2， 工作流开发

进入`crawler`文件夹中，参照`workflow_example.py`编写自己的工作流

```python

class WorkflowExample(Workflow):
    def __init__(self, domain: str, start_path: str, end_path_regex: str):
        super().__init__(domain, start_path, end_path_regex)

    @register_crawler
    def main(self) -> celery.result.AsyncResult:
        print(f"Start crawling from: {self.domain + self.start_path}")
        param = self.param_base.model_copy(
            update={
                'tag': 'chapter',
                'url_path': self.start_path
            }
        )
        return step1.delay(param)

    def data_processing(self, data):
        ...
```
首先继承`Workflow`类，然后实现`main`方法，`main`方法是工作流的入口，
通过`register_crawler`装饰器注册爬虫任务。`main`方法返回一个`celery`任务对象。当这个任务标记完成时，表示任务分发完毕


### 3. 初始化配置文件
修改配置请修改.env文件

```shell
$ cp .env.example .env
```


### 4. 一键启动

按照以下命令启动分布式节点

```shell
$ bash scripts/start_cellery.sh
```

按照以下命令启动服务

```shell
$ python main.py
```

## 项目进度

✅完成请求模块

✅初步完成解析模块，后续会集成大语言模型

✅初步完成工作流模板，后续会不断精简并让用户更方便的使用

⌛️ 完成日志记录模块

⌛️ 完成调度器模块，用于调度工作流

⌛️ 完成数据处理模块

⌛️ 完成数据存储模块

⌛️ 完成前端管理模块

⌛️ 完成节点管理模块

......


## 感谢以下项目
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=celery&repo=celery)](https://github.com/celery/celery)

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=mher&repo=flower)](https://github.com/mher/flower)

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=fastapi&repo=fastapi)](https://github.com/fastapi/fastapi)


