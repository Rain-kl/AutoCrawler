import asyncio
from functools import wraps
from time import perf_counter
from typing import Any, Callable
from loguru import logger


def get_time(func: Callable) -> Callable:
    @wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        start_time: float = perf_counter()
        result: Any = func(*args, **kwargs)
        end_time: float = perf_counter()

        logger.debug(f'"{func.__name__}()" took {end_time - start_time:.3f} seconds to execute')
        return result

    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        start_time: float = perf_counter()
        result: Any = await func(*args, **kwargs)
        end_time: float = perf_counter()

        logger.debug(f'"{func.__name__}()" took {end_time - start_time:.3f} seconds to execute')
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
