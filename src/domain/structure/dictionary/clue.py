class clue:
    
    _clue: str
    _score: int
    
    def __init__(self, clue: str, score: str) -> None:
        self._clue = clue
        self._score = score
        
    def clue(self) -> str:
        return self._clue
        
    def score(self) -> int:
        return self._score
    
    def struct(self) -> dict[str,str]:
        return {
            "clue": self._clue,
            "score": self._score        
        }