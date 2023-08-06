import asyncio
import inspect
from functools import partial, wraps
from typing import Awaitable, Callable, TypeVar

Ret = TypeVar("Ret")


def to_async(sync_func: Callable[..., Ret]) -> Callable[..., Awaitable[Ret]]:
    "Wraps a synchronous function into an asynchronous callable."

    if inspect.isawaitable(sync_func):
        raise TypeError("already an awaitable")

    if not callable(sync_func):
        raise TypeError("not a callable")

    @wraps(sync_func)
    async def _async_func(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_running_loop()
        pfunc = partial(sync_func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return _async_func
