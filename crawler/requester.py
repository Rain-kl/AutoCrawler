# crawler/requester.py

import requests
from config.settings import settings
from  .logger import logger

class Requester:
    def __init__(self):
        self.user_agent = settings.user_agent
        self.timeout = settings.request_timeout

    def send_request(self, url, method="GET", headers=None, params=None, data=None):
        if headers is None:
            headers = {}
        headers['User-Agent'] = self.user_agent

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None


# 在项目中使用 Requester
requester = Requester()