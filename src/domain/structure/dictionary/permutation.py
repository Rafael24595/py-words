from domain.structure.dictionary.clue import clue
from domain.structure.dictionary.clues import clues
from domain.structure.dictionary.permutation_result import permutation_result

KEY_BASE: str = "PERMUTATION"

class permutation():
    
    _base: str
    _result: list[str]
    _clues: clues
    
    def __init__(self, base: str, result: list[str]) -> None:
        self._base = base
        self._result = result
        self.__build_clues()
        
    def __build_clues(self):
        unused_chars: list[str] = self.__unused_characters()
        self._clues = clues()
        self._clues.add("length", "Number of permutations: " + str(len(self._result)), 75)
        self._clues.add("unused-chars-len", "Total unused characters: " + str(len(unused_chars)), 75)
        self._clues.add("unused-chars", "Unused characters list: " + str(unused_chars), 75)
        for index, word in enumerate(self._result):
            i: str = str(index + 1)
            self._clues.add("result-" + i, "Word " + i + ": " + word, 100)
        
    def get_base(self) -> str:
        return self._base
    
    def get_result(self) -> list[str]:
        return self._result
    
    def evalue_result(self, words: list[str]) -> permutation_result:
        found: list[str] = []
        forgotten: list[str] = self._result.copy()
        mistaked: list[str] = words.copy()
        for word in self._result:
            if word in words:
                found.append(word)
                forgotten.remove(word)
                mistaked.remove(word)
        return permutation_result(found, forgotten, mistaked)
    
    def find_different_clues(self, clues: list[str]) -> list[clue]:
        return self._clues.filter(clues, True)
    
    def find_clues(self, clues: list[str]) -> list[clue]:
        return self._clues.filter(clues, False)
    
    def key(self) -> str:
        return KEY_BASE + "#" + self._base
    
    def __unused_characters(self):
        chars: list[str] = []
        for char in self._base:
            for word in self._result:
                if char not in word and char not in chars:
                    chars.append(char)
        return chars
    
    def struct(self) -> dict[str,str]:
        return {
            "base": self._base,
            "result": self._result,
            "clues": self._clues.struct()
        }