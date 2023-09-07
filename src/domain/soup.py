from abc import ABC, abstractmethod

class soup(ABC):

    @abstractmethod
    async def generate_soup(self) -> None:
        pass