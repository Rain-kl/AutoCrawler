# crawler/requester.py

import random
from typing import Union
import chardet
import httpx

from config.settings import settings
from config.logging_config import logger
from .decorator import cached_function



class Headers:
    def __init__(self, headers: dict = None):
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        self.headers = headers

    def __str__(self):
        return self.headers

    def json(self):
        return self.headers

    def update(self, headers):
        self.headers.update(headers)


class ProxyConfig:
    def __init__(
            self,
            host: str = settings.proxy_host,
            port: Union[str, int, list] = settings.proxy_port
    ):
        """
        :param host: 127.0.0.1
        :param port: 7890
        """
        self.host = host
        self.port = port

    def get_proxy(self):
        if not self.host or not self.port:
            return None
        if isinstance(self.port, list):
            port = random.choice(self.port)
        else:
            port = self.port
        HTTP_PROXY = f"http://{self.host}:{port}"
        return {'http://': HTTP_PROXY, 'https://': HTTP_PROXY}


class Requester:
    def __init__(
            self,
            headers: dict = None,
            timeout: int = settings.request_timeout,
            proxy_pool: ProxyConfig = ProxyConfig(),
            # cookie_pool: list = None,  # todo: cookie_pool
            # proxies: dict = None
    ):
        if headers is None:
            headers = Headers()
        self.headers = headers
        self.timeout = timeout
        self.proxy_pool = proxy_pool
        self.cookie_pool = None  # todo: cookie_pool
        self.proxies = None
        self.client = None

    def update_client(self):
        if self.cookie_pool:
            self.headers['Cookie'] = random.choice(self.cookie_pool)
        if self.proxy_pool:
            self.proxies = self.proxy_pool.get_proxy()

        self.client = httpx.Client(proxies=self.proxies, headers=self.headers.json(), verify=True)

    def close_client(self):
        if self.client:
            self.client.aclose()

    def __del__(self):
        self.close_client()

    # @cached_function(timeout=600)
    def send_request_sync(self, url, method="GET", headers=None, params=None, data=None, json=None, encoding=None):
        try:
            if headers is None:
                headers = self.headers
            else:
                headers.update(self.headers)
            if not self.client:
                self.update_client()
            response = self.client.request(
                method=method,
                url=url,
                headers=headers.json(),
                params=params,
                data=data,
                timeout=self.timeout,
                json=json,
                follow_redirects=True
            )
            if encoding:
                response.encoding = encoding
            else:
                detected_encoding = chardet.detect(response.content)['encoding']
                response.encoding = detected_encoding if detected_encoding else 'utf-8'

            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"Request failed: {e}")
            # log_debug.trace(e)  # 确保 log_debug.trace(e) 是定义在某处的
            self.update_client()
            raise


requester = Requester()
