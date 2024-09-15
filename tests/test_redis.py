from crawler.utils import redis


def test_redis():
    redis.set('test', 'test')
    rsp = redis.get('test')
    assert rsp == b'test'
