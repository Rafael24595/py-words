from domain.dictionary import dictionary
from domain.permutation import permutation

class dictionary_memory(dictionary):
    
    def __init__(self, *args: str) -> None:
        pass
    
    async def generate_permutation(self) -> permutation:
        return permutation("XYZ", ["XYZ", "YXZ", "ZXY", "XZY", "YZX", "ZYX"]) 
    
    async def find_random(self, count: int) -> list[str]:
        return super().find_random(count)