# crawler/workflow.py

from .scheduler import scheduler
from .requester import requester
from .parser import parser


class WorkflowEngine:
    def __init__(self, start_url, page_limit=10):
        self.start_url = start_url
        self.page_limit = page_limit
        self.visited = set()
        self.to_visit = [start_url]

    def start_workflow(self):
        while self.to_visit and len(self.visited) < self.page_limit:
            url = self.to_visit.pop(0)
            if url not in self.visited:
                self.process_page(url)

    def process_page(self, url):
        response = requester.send_request(url)
        if response:
            soup = parser.parse_html(response.content)
            links = parser.extract_links(soup)
            self.to_visit.extend(links)
            self.visited.add(url)
            self.handle_data(soup)

    def handle_data(self, soup):
        # 用户可以在这里添加数据处理逻辑
        print(f"Processed data from: {soup.title.string}")


# 在项目中使用 WorkflowEngine
workflow = WorkflowEngine(start_url='http://example.com')
workflow.start_workflow()