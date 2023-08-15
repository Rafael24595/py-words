class permutation():
    
    _base: str
    _result: list[str]
    
    def __init__(self, base: str, result: list[str]) -> None:
        self._base = base
        self._result = result
        
    def get_base(self) -> str:
        return self._base
    
    def get_result(self) -> list[str]:
        return self._result