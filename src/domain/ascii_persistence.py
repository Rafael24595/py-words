from abc import ABC, abstractmethod
from commons.optional import optional

from domain.structure.ascii.ascii_image import ascii_image

class ascii_persistence(ABC):

    @abstractmethod
    async def put(self, form: ascii_image) -> ascii_image:
        pass
    
    @abstractmethod
    async def take(self, key: str) -> optional[ascii_image]:
        pass
    
    @abstractmethod
    async def takeAll(self) -> list[ascii_image]:
        pass