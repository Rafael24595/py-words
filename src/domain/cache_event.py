import time
from typing import Generic, TypeVar

T = TypeVar('T')

class cache_event(Generic[T]):
    
    __key: str
    __reference: str
    __timestamp: int
    __data: T
    
    def __init__(self, key: str, reference: str, data: T) -> None:
        self.__key = key
        self.__reference = reference
        self.__timestamp = round(time.time() * 1000)
        self.__data = data
        
    def key(self) -> str:
        return self.__key
    
    def reference(self) -> str:
        return self.__reference
    
    def timestamp(self) -> int:
        return self.__timestamp
    
    def data(self) -> T:
        return self.__data