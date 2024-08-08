# crawler/workflow.py

from .scheduler import scheduler
from .requester import requester
from .parser import parser


class WorkflowEngine:
    def __init__(
            self,
            start_url="/book/166492/",
            target_path="/book/166492/.*html",
            target_type="text",
            path_to_target="/book/166492/.*html|/book/166492 -> /book/166492/.*html"
    ):
        self.start_url = start_url
        self.target_path = target_path
        self.target_type = target_type
        self.path_to_target = path_to_target
        self.visited = set()
        self.to_visit = [start_url]

    def start_workflow(self):
        pass

    def parse_directory_page(self, url):
        pass

    def handle_data(self, soup):
        # 用户可以在这里添加数据处理逻辑
        print(f"Processed data from: {soup.title.string}")


# 在项目中使用 WorkflowEngine
workflow = WorkflowEngine(start_url='http://example.com')
workflow.start_workflow()
