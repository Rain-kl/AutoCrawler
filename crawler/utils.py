from celery.result import AsyncResult

def get_celery_result(task_id):
    result=AsyncResult(task_id)
    if result.ready():
        return result.get()


def parse_url(domain, url):
    if url.startswith('http'):
        return url
    return domain + url

if __name__ == '__main__':
    get_celery_result('fc561de3-459d-4a70-a1b5-cd5e4b9a9975')