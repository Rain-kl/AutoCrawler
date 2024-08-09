# crawler/parser.py
import httpx

from plugins.auto_parser import AutoParser


class Parser:
    def __init__(self, date: httpx.Response | str | list | dict):
        self.json_data: dict | list | None = None
        self.response_text: str | None = None

        if isinstance(date, httpx.Response):
            assert date.status_code == 200, f"response status code is not 200, got {date.status_code}"
            try:
                self.json_data = date.json()
            except:
                self.response_text = date.text
        if isinstance(date, str):
            self.response_text = date

        if isinstance(date, list) or isinstance(date, dict):
            self.json_data = date

    @property
    def json(self):
        return JsonParser(self.json_data)

    @property
    def html(self):
        return HTMLParser(self.response_text)


class JsonParser:
    def __init__(self, json_data: dict | list):
        self.json_data = json_data

    def your_method(self):
        pass


class HTMLParser(AutoParser):  # 使用AutoParser自动解析HTML
    def __init__(self, html: str):
        super().__init__(html)

    def your_method(self):
        pass


if __name__ == '__main__':
    with open('../test.html', 'r') as f:
        sample_html = f.read()

    p = Parser(sample_html)
    html_struct = p.html.extract_structure()
    # max_node = parser.html.find_maximum()
    max_node = p.html.find(tag='div')
    # output:
    # print(html_struct.model_dump_json(indent=2))
    print(max_node)
    for node in max_node:
        print("output: ", end='')
        print(node)

    # print(max_node.extract_all_text(ignore_elements=['dt']))
    # print(len(max_node.extract_all_url()))
