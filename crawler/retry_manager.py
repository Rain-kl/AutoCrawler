# crawler/retry_manager.py

from tenacity import retry, stop_after_attempt, wait_fixed
from .requester import requester

class RetryManager:
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def send_request_with_retry(self, url, method="GET", headers=None, params=None, data=None):
        return requester.send_request(url, method, headers, params, data)

# 在项目中使用 RetryManager
retry_manager = RetryManager()