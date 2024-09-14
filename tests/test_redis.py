from crawler.utils import get_redis


def test_redis():
    redis = get_redis()
    redis.set('test', 'test')
    rsp = redis.get('test')
    assert rsp == b'test'
