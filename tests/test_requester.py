# tests/test_requester.py


from crawler.requester import Requester


def test_send_request():
    requester = Requester()
    url = "http://m.gdsoftga.com/book/46553/"
    response = requester.send_request_sync(url)
    assert response is not None
    assert response.status_code == 200
