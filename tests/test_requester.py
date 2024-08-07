# tests/test_requester.py
import pytest

from crawler.requester import Requester

@pytest.mark.asyncio
async def test_send_request():
    requester = Requester()
    url = "http://m.gdsoftga.com/book/166492/"

    response = await requester.send_request(url)
    assert response is not None
    assert response.status_code == 200

def test_send_request_failure():
    requester = Requester()
    url = "http://nonexistent-url"

    response = requester.send_request(url)
    assert response is None