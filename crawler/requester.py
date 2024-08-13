# crawler/requester.py
import asyncio

import httpx
import chardet
import random
import logging
from typing import Union
from loguru import logger as log_debug
from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log
from .headers import generate_headers
from .decorator import cached_function
from config.settings import settings
from .logger import logger


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
            headers: dict = generate_headers(),
            timeout: int = settings.request_timeout,
            proxy_pool: ProxyConfig = ProxyConfig(),
            # cookie_pool: list = None,  # todo: cookie_pool
            # proxies: dict = None
    ):
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

        self.client = httpx.Client(proxies=self.proxies, headers=self.headers, verify=True)

    def close_client(self):
        if self.client:
            self.client.aclose()

    # @retry(stop=stop_after_attempt(5), wait=wait_fixed(3), before_sleep=before_sleep_log(logger, logging.INFO))
    @cached_function(timeout=600)
    # @get_time
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
                headers=headers,
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
