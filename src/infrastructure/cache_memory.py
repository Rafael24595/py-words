import threading
from typing import Any
from commons.optional import optional
from domain.cache import cache
from domain.cache_event import cache_event

class cache_memory(cache):
    
    NAME: str = "cache_memory"
    
    __lock: threading.Lock
    __cache: dict[str, cache_event[Any]]
    
    def __init__(self, *args: dict[str, str]) -> None:
        self.__lock = threading.Lock()
        self.__cache = {}
    
    async def exists(self, key: str) -> bool:
        return not self.__cache.get(key) == None
    
    async def get(self, key: str) -> optional[cache_event[Any]]:
        return optional.some(self.__cache.get(key))
    
    async def put(self, key: str, reference: str, value: Any) -> cache_event[Any]:
        self.__lock.acquire()
        event = cache_event(key, reference, value)
        self.__cache[key] = event
        self.__lock.release()
        return event
    
    async def delete(self, key: str) -> optional[cache_event[Any]]:
        self.__lock.acquire()
        value = self.__cache.pop(key)
        self.__lock.release()
        return optional.some(value)