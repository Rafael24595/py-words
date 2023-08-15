from typing import Any

from abc import ABC, abstractmethod

from commons.optional import optional

class cache(ABC):

    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    async def get(self, key: str) -> optional[Any]:
        pass

    @abstractmethod
    async def put(self, key: str, value: Any) -> Any:
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> optional[Any]:
        pass