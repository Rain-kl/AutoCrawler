from typing import Any

import httpx
from pydantic import BaseModel


class ResponseModel(BaseModel):
    tag: str
    response: Any

    class Config:
        arbitrary_types_allowed = True

    def __json__(self):
        return self.model_dump()


class Param(BaseModel):
    tag: str = 'example'  # 任务标签
    domain: str = 'https://example.com'  # 网站域名
    url_path: str = '/example'  # 网站路径
    url: str = 'https://example.com/example'  # 完整网址, 由domain和url_path自动拼接而成
    end_path_regex: str = '/example/.*html'  # 结束路径正则表达式
    workflow_id: str  # 工作流ID
    url_params: dict = {
        "param": None,
        "data": None,
        "json": None,
    }

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if self.url_path.startswith('http'):
            raise ValueError('url_path should not start with http')
        if not self.domain.startswith('http'):
            raise ValueError('domain should start with http')
        if not self.url_path.startswith('/'):
            self.url_path = '/' + self.url_path
        self.domain = self.domain.rstrip('/')
        self.url = self.domain + self.url_path

    def __json__(self):
        return self.model_dump()
