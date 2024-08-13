from typing import Any

import httpx
from pydantic import BaseModel


class ResponseModel(BaseModel):
    tag: str
    response: httpx.Response | str

    class Config:
        arbitrary_types_allowed = True

    def __json__(self):
        return self.model_dump()


class Param(BaseModel):
    tag: str = 'example'
    domain: str = 'https://example.com'
    url_path: str = '/example'
    url: str = 'https://example.com/example'
    end_path_regex: str = '/example/.*html'
    workflow_id: str

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
