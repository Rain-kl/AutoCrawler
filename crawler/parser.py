# crawler/parser.py
from typing import List, Dict, AnyStr
from typing import Union

import httpx
import requests

from plugins.auto_parser import AutoParser


class Parser:
    def __init__(
            self,
            date: Union[httpx.Response, requests.Response, AnyStr, List, Dict],
            type_: str = "response"
    ):
        self.json_data: dict | list | None = None
        self.response_text: str | None = None
        if type_ == "response":
            assert isinstance(date, object), f"date should be object, got {type(date)}"
            assert date.status_code == 200, f"response status code is not 200, got {date.status_code}"
            try:
                self.json_data = date.json()
            except Exception as e:
                self.response_text = date.text
        elif type_ == "text":
            if isinstance(date, str):
                self.response_text = date
            else:
                raise ValueError(f"date should be str, got {type(date)}")
        elif type_ == "json":
            if isinstance(date, list) or isinstance(date, dict):
                self.json_data = date
            else:
                raise ValueError(f"date should be list or dict, got {type(date)}")
        else:
            raise ValueError(f"type_ should be response, text or json, got {type_}")

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
