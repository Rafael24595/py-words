class permutation_result:
    
    _found: list[str]
    _forgotten: list[str]
    _mistaked: list[str]
    
    def __init__(self, found: list[str], forgotten: list[str], mistaked: list[str]) -> None:
        self._found = found
        self._forgotten = forgotten
        self._mistaked = mistaked
        
    def found(self) -> list[str]:
        return self._found
    
    def forgotten(self) -> list[str]:
        return self._forgotten
    
    def mistaked(self) -> list[str]:
        return self._mistaked