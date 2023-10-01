import threading
from typing import Any, TypeVar

from commons.configuration.dependency.dependency_container import dependency_container
from commons.optional import optional
from domain.cache import cache
from domain.cache_event import cache_event

T = TypeVar('T')

class session():
    
    __id: str
    
    def __init__(self, id) -> None:
        self.__id = id
    
    def get_id(self) -> str:
        return self.__id
        
    async def store(self, key: str, value: T) -> optional[T]:
        cache_service: optional[cache] = dependency_container.instance().get_cache()
        if(cache_service.is_some()):
            session_key: str = self.generate_key(key)
            value = await cache_service.unwrap().put(session_key, self.__id, value)
            return optional.some(value)
        return optional.none()
    
    async def unstore(self, key: str) -> optional[cache_event[T]]:
        cache_service: optional[cache] = dependency_container.instance().get_cache()
        if(cache_service.is_some()):
            session_key: str = self.generate_key(key)
            return await cache_service.unwrap().get(session_key)
        return optional.none()
    
    def generate_key(self, key: str) -> str:
        return self.__id + "#" + key