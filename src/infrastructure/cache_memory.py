import threading
from typing import Any
from commons.optional import optional
from domain.cache import cache

class cache_memory(cache):
    
    __lock: threading.Lock
    __cache: dict[str, Any]
    
    def __init__(self, *args: str) -> None:
        self.__lock = threading.Lock()
        self.__cache = {}
    
    async def exists(self, key: str) -> bool:
        return not self.__cache.get(key) == None
    
    async def get(self, key: str) -> optional[Any]:
        return optional.some(self.__cache.get(key))
    
    async def put(self, key: str, value: Any) -> Any:
        self.__lock.acquire()
        self.__cache[key] = value
        self.__lock.release()
        return value
    
    async def delete(self, key: str) -> optional[Any]:
        self.__lock.acquire()
        value = self.__cache.pop(key)
        self.__lock.release()
        return optional.some(value)