from functools import partial
from typing import Awaitable, Callable, Generic, List, TypeVar, Union

from anyio.to_thread import run_sync
from esmerald.utils.helpers import is_async_callable
from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


class AsyncCallable(Generic[P, T]):
    __slots__ = ("args", "kwargs", "fn")

    def __init__(self, fn: Callable[P, T]):
        self.fn: Callable[P, Awaitable[T]]
        if is_async_callable(fn):
            self.fn = fn
        else:
            self.fn = partial(run_sync, fn)  # type:ignore[assignment]

    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return await self.fn(*args, **kwargs)


def as_async_callable_list(value: Union[Callable, List[Callable]]) -> List[AsyncCallable]:
    if not isinstance(value, list):
        return [AsyncCallable(value)]
    return [AsyncCallable(v) for v in value]
