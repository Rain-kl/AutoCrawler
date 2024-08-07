# tests/test_requester.py

from crawler.requester import Requester

def test_send_request():
    requester = Requester()
    url = "http://example.com"

    response = requester.send_request(url)
    assert response is not None
    assert response.status_code == 200

def test_send_request_failure():
    requester = Requester()
    url = "http://nonexistent-url"

    response = requester.send_request(url)
    assert response is None