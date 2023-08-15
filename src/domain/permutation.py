KEY_BASE: str = "PERMUTATION"

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
    
    def key(self) -> str:
        return KEY_BASE + "#" + self._base
    
    def struct(self) -> str:
        return {
            "base": self._base,
            "result": self._result
        }