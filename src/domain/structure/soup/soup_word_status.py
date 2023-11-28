from typing import Any
from domain.structure.soup.soup_character import soup_character

class soup_word_status:
    
    __word: str
    __resolved: bool
    
    def __init__(self, word: str, resolved: bool) -> None:
        self.__word = word
        self.__resolved = resolved
    
    def word(self) -> str:
        return self.__word
    
    def is_resolved(self) -> bool:
        return self.__resolved
    
    def as_dto(self) -> dict[str,Any]:
        dto: dict[str,Any] = {}
        dto["word"] = self.__word
        dto["resolved"] = self.__resolved
        return dto