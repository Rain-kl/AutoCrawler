import asyncio
import inspect
from functools import wraps
from time import perf_counter
from typing import Any, Callable

import diskcache

from config.logging_config import logger
from .celery import celery_app
from .model import Param

cache = diskcache.Cache('.cache',)


# 创建一个缓存装饰器
def cached_function(timeout):
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            async def async_wrapper(self, *args, **kwargs):
                key = f'{func.__name__}:{args}:{kwargs}'
                # print(key)
                result = cache.get(key)
                if result is None:
                    result = await func(self, *args, **kwargs)
                    cache.set(key, result, expire=timeout)
                else:
                    logger.debug(f'cache hit: {key}')
                return result

            return async_wrapper
        else:
            def wrapper(self, *args, **kwargs):
                key = f'{func.__name__}:{args}:{kwargs}'
                result = cache.get(key)
                if result is None:
                    result = func(self, *args, **kwargs)
                    cache.set(key, result, expire=timeout)
                else:
                    logger.debug(f'cache hit: {key}')
                return result

            return wrapper

    return decorator


def get_time(func: Callable) -> Callable:
    @wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        start_time: float = perf_counter()
        result: Any = func(*args, **kwargs)
        end_time: float = perf_counter()

        logger.info(f'"{func.__name__}()" took {end_time - start_time:.3f} seconds to execute')
        return result

    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        start_time: float = perf_counter()
        result: Any = await func(*args, **kwargs)
        end_time: float = perf_counter()

        logger.info(f'"{func.__name__}()" took {end_time - start_time:.3f} seconds to execute')
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def listen_taskpool_async(func):
    @wraps(func)
    def wrapper(params, *args, **kwargs):
        if isinstance(params, dict):
            params = Param(**params)
        return asyncio.run(func(params, *args, **kwargs))

    return celery_app.task(wrapper)
