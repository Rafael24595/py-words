from typing import Any
from domain.soup_panel.soup_character import soup_character
from domain.soup_panel.soup_panel import soup_panel
from domain.soup_panel.soup_word import soup_word

class soup_builder:
    
    @classmethod
    def build(cls, dto: Any) -> soup_panel:
        words: list[soup_word] = cls.__build_words(dto.words)
        panel: list[list[str]] = dto.panel
        return soup_panel(words, panel)
    
    @classmethod
    def __build_words(cls, dtos: list[Any]) -> list[soup_word]:
        words: list[soup_word] = []
        for dto in dtos:
            word: soup_word = cls.__build_word(dto)
            words.append(word)
        return words
    
    @classmethod
    def __build_word(cls, dto: Any) -> list[soup_word]:
        characters:  dict[soup_character] = cls.__build_characters(dto.characters)
        orientation: str = dto.orientation
        word: str = dto.word
        return soup_word(characters, orientation, word)
    
    @classmethod
    def __build_characters(cls, dtos: list[Any]) -> dict[soup_character]:
        characters: dict[soup_character] = {}
        for dto in dtos:
            character: soup_character = cls.__build_character(dto)
            characters[character.key()] = character
        return characters
    
    @classmethod
    def __build_character(cls, dto: Any) -> list[soup_character]:
        return soup_character(dto.character, dto.x, dto.y)