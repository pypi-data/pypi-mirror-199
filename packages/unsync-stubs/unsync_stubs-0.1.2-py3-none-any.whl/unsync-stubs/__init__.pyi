"""Type stubs for unsync."""

from asyncio import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from threading import Thread
from typing import Any, Callable, Dict, Generator, Generic, TypeVar

T = TypeVar('T')


class Unfuture(Generic[T]):
    @staticmethod
    def from_value(value: Any) -> "Unfuture[T]":
        ...
    
    def __init__(self, future: Any = ...) -> None:
        ...
    
    def __iter__(self) -> Generator[Any, None, Any]:
        ...
    
    __await__ = ...
    def result(self, *args: Any, **kwargs: Any) -> T:
        ...
    
    def done(self) -> bool:
        ...
    
    def set_result(self, value: Any) -> Any:
        ...
    
    @unsync
    async def then(self, continuation: Any):
        ...


class unsync_meta(type):
    @property
    def loop(cls) -> AbstractEventLoop:
        ...
    
    @property
    def thread(cls) -> Thread:
        ...
    
    @property
    def process_executor(cls) -> ProcessPoolExecutor:
        ...
    


class unsync(metaclass=unsync_meta):
    thread_executor: ThreadPoolExecutor = ...
    process_executor: ProcessPoolExecutor = ...
    unsync_functions: Dict[Any, Any] = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...
    
    @property
    def cpu_bound(self) -> bool:
        ...
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    
    def __get__(self, instance: Any, owner: Any) -> Callable[..., Any]:
        ...
