from commons.optional import optional
from domain.structure.dictionary.clue import clue

class clues:
    
    _clues: dict[str,clue]
    
    def __init__(self) -> None:
        self._clues= {}
        
    def add(self, key: str, value:str, score: int):
        self._clues[key] = clue(value, score)
        
    def get(self, key) -> optional[clue]:
        return optional.some(self._clues.get(key))
    
    def filter(self, clues: list[str], not_in: bool) -> list[clue]:
        new_clues: list[clue] = []
        for key in self._clues:
            cl = self._clues[key]
            if not_in and cl.clue() not in clues:
                new_clues.append(cl)
            if not not_in and cl.clue() in clues:
                new_clues.append(cl)
        return new_clues
    
    def struct(self) -> dict[str,str]:
        struct: dict[str,dict] = {}
        for key in self._clues:
            struct[key] = self._clues[key].struct()
        return struct