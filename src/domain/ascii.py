from abc import ABC, abstractmethod

from domain.ascii_form import ascii_form
from domain.ascii_image import ascii_image

class ascii(ABC):

    @abstractmethod
    async def generate_ascii(self, form: ascii_form) -> ascii_image:
        pass
    
    @abstractmethod
    async def take(self, key: str) -> ascii_image:
        pass
    
    @abstractmethod
    async def takeAll(self) -> list[ascii_image]:
        pass