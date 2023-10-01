from typing import Any

from abc import ABC, abstractmethod

from commons.optional import optional
from domain.cache_event import cache_event

class cache(ABC):

    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    async def get(self, key: str) -> optional[cache_event[dict[str, str]]]:
        pass

    @abstractmethod
    async def put(self, key: str, reference: str, value: dict[str, str]) -> cache_event[dict[str, str]]:
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> optional[cache_event[dict[str, str]]]:
        pass