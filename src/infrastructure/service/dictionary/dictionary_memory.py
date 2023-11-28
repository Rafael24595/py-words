from domain.dictionary import dictionary
from domain.structure.dictionary.permutation import permutation

class dictionary_memory(dictionary):
    
    NAME: str = "dictionary_memory"
    
    def __init__(self, args: dict[str, str]) -> None:
        pass
    
    async def generate_permutation(self, combolen: int) -> permutation:
        return permutation("XAYZ", ["XYZ", "YXZ", "ZXY", "XZY", "YZX", "ZYX"]) 
    
    async def generate_target_permutation(self, combo: str) -> permutation:
        return permutation(combo, ["CALCULATE"]) 
    
    async def find_random(self, count: int) -> list[str]:
        mockList = []
        for i in range(count):
            mockList.append("Word_" + str(i))
        return mockList