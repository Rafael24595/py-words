from abc import ABC, abstractmethod

from domain.permutation import permutation

class dictionary(ABC):

    @abstractmethod
    async def generate_permutation(self, combolen: int) -> permutation:
        pass
    
    @abstractmethod
    async def generate_target_permutation(self, combo: str) -> permutation:
        pass

    @abstractmethod
    async def find_random(self, count: int) -> list[str]:
        pass