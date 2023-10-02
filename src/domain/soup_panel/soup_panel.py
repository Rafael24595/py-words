from typing import Any
from domain.soup_panel.soup_character import soup_character
from domain.soup_panel.soup_word import soup_word

class soup_panel:
    
    __panel: list[list[str]]
    __words: list[soup_word]
    
    def __init__(self, panel: list[list[str]], words: list[soup_word]) -> None:
        self.__panel = panel
        self.__words = words
        
    def panel(self) -> list[list[str]]:
        return self.__panel
    
    def words(self) -> list[soup_word]:
        return self.__words
    
    def check_characters(self, characters: list[soup_character]) -> list[str]:
        coincidence: dict[str,list[str]] = {}
        for character in characters:
            words = self.__words_includes(character)
            for word in words:
                if word.includes(character):
                    if coincidence.get(word.word()) is None:
                        coincidence[word.word()] = []
                    coincidence[word.word()].append(character.key())
        return self.__check_words(coincidence)
        
    def __words_includes(self, character: soup_character) -> list[soup_word]:
        words = []
        for word in self.__words:
            if character.character() in word.word():
                words.append(word)
        return words
    
    def __check_words(self, coincidence: dict[str,list[str]]) -> list[str]:
        words = self.__get_words(list(coincidence.keys()))
        resolved: list[str] = []
        for word in words:
            if word.check_characters(coincidence[word.word()]):
                word.mark_as_resolved()
                resolved.append(word.word())
        return resolved
    
    def __get_words(self, raw_words: list[str]) -> list[soup_word]:
        words = []
        for word in self.__words:
            if word.word() in raw_words:
                words.append(word)
        return words
    
    def as_dto(self) -> dict[str,Any]:
        dto: dict[str,Any] = {}
        dto["panel"] = self.__panel
        dto["words"] = []
        for word in self.__words:
            dto["words"].append(word.as_dto())
        return dto