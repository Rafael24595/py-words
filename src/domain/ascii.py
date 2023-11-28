from abc import ABC, abstractmethod
from commons.optional import optional

from domain.ascii_form import ascii_form
from domain.ascii_gray_scale import ascii_gray_scale
from domain.ascii_image import ascii_image
from domain.ascii_persistence import ascii_persistence

class ascii(ABC):

    @abstractmethod
    def enablePersistence(self, persistence: ascii_persistence):
        pass

    @abstractmethod
    async def get_gray_scales(self) -> list[ascii_gray_scale]:
        pass

    @abstractmethod
    async def generate_ascii(self, form: ascii_form) -> ascii_image:
        pass
    
    @abstractmethod
    async def take(self, key: str) -> optional[ascii_image]:
        pass
    
    @abstractmethod
    async def takeAll(self) -> list[ascii_image]:
        pass