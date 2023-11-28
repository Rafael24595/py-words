from typing import Any
from domain.structure.soup.soup_character import soup_character
from domain.structure.soup.soup_position import soup_position
from domain.structure.soup.soup_word import soup_word
from domain.structure.soup.soup_word_status import soup_word_status

class soup_panel:
    
    __panel: list[list[soup_position]]
    __words: list[soup_word]
    
    def __init__(self, panel: list[list[soup_position]], words: list[soup_word]) -> None:
        self.__panel = panel
        self.__words = words
        
    def panel(self) -> list[list[soup_position]]:
        return self.__panel
    
    def words(self) -> list[soup_word]:
        return self.__words
    
    def resolved_words(self) -> list[str]:
        words: list[str] = []
        for word in self.__words:
            if word.is_resolved():
                words.append(word.word())
        return words
    
    def words_status(self) -> list[dict[str,Any]]:
        words: list[str] = []
        for word in self.__words:
            word_status: soup_word_status = soup_word_status(word.word(), word.is_resolved())
            words.append(word_status.as_dto())
        return words
    
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
            if not word.is_resolved() and character.character() in word.word():
                words.append(word)
        return words
    
    def __check_words(self, coincidence: dict[str,list[str]]) -> list[str]:
        words = self.__get_words(list(coincidence.keys()))
        resolved: list[str] = []
        for word in words:
            if word.check_characters(coincidence[word.word()]):
                word.mark_as_resolved()
                self.__check_positions(word.characters().values())
                resolved.append(word.word())
        return resolved
    
    def __check_positions(self, characters: list[soup_character]) -> list[str]:
        for character in characters:
            position: soup_position = self.__panel[character.y()][character.x()]
            position.mark_as_resolved()
    
    def __get_words(self, raw_words: list[str]) -> list[soup_word]:
        words = []
        for word in self.__words:
            if word.word() in raw_words:
                words.append(word)
        return words
    
    def as_dto(self) -> dict[str,Any]:
        dto: dict[str,Any] = {}
        dto["panel"] = []
        for row in self.__panel:
            panel_row: list[dict[str,Any]] = []
            for position in row:
                panel_row.append(position.as_dto())
            dto["panel"].append(panel_row)
        dto["words"] = []
        for word in self.__words:
            dto["words"].append(word.as_dto())
        return dto