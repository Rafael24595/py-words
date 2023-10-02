from typing import Any
from domain.soup_panel.soup_character import soup_character

class soup_word:
    
    __characters: dict[str, soup_character]
    __orientation: str
    __word: str
    __resolved: bool
    
    def __init__(self, characters: dict[str, soup_character], orientation: str, word: str, resolved: bool) -> None:
        self.__characters = characters
        self.__orientation = orientation
        self.__word = word
        self.__resolved = resolved
        
    def characters(self) -> dict[str, soup_character]:
        return self.__characters
    
    def orientation(self) -> str:
        return self.__orientation
    
    def word(self) -> str:
        return self.__word
    
    def mark_as_resolved(self):
        self.__resolved = True
    
    def mark_as_unresolved(self):
        self.__resolved = False
    
    def is_resolved(self) -> bool:
        return self.__resolved
    
    def includes(self, character: soup_character) -> bool:
        key = character.key()
        word = self.__characters.get(key)
        return word is not None
    
    def check_characters(self, characters: list[str]) -> bool:
        if len(characters) != len(self.__characters.keys()):
            return False
        for character in self.__characters.keys():
            if character in characters:
                characters.remove(character)
        return len(characters) == 0
    
    def as_dto(self) -> dict[str,Any]:
        dto: dict[str,Any] = {}
        dto["orientation"] = self.__orientation
        dto["word"] = self.__word
        dto["resolved"] = self.__resolved
        dto["characters"] = {}
        for character in self.__characters:
            dto["characters"][character] = self.__characters[character].as_dto()
        return dto