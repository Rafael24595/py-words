from abc import ABC, abstractmethod

from domain.permutation import permutation

class dictionary(ABC):

    @abstractmethod
    async def generate_permutation(self) -> permutation:
        pass
    
    @abstractmethod
    async def generate_target_permutation(self, target: str) -> permutation:
        pass

    @abstractmethod
    async def find_random(self, count: int) -> list[str]:
        pass