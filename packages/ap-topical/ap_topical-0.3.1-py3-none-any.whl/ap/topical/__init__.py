import asyncio
import functools
from collections import defaultdict
from typing import Callable, Dict, List, Any

__event_map:Dict[str,List[Callable]] = defaultdict(list)


def subscribe(event, callback) -> None:
    global __event_map
    __event_map[event].append(callback)


async def publish(event, payload) -> None:
    tasks = [cb(payload) for cb in __event_map[event]]
    await asyncio.gather(*tasks)

class event:
    def __init__(self, event:str):
        self.event = event
        self.decorator = self._decorator(event)

    def __call__(self, fn:Callable):
        return self.decorator(fn)

    def _decorator(self, event:str):
        def wrapped(fn:Callable):
            @functools.wraps(fn)
            async def wrapper(payload:Any):
                return await fn(payload)

            subscribe(event, fn)
            return wrapper
        return wrapped
