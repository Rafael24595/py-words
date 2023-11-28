from typing import Any
from domain.structure.soup.soup_character import soup_character
from domain.structure.soup.soup_panel import soup_panel
from domain.structure.soup.soup_position import soup_position
from domain.structure.soup.soup_word import soup_word

class soup_builder:
    
    @classmethod
    def build_from_resume_dto(cls, dto: Any) -> soup_panel:
        words: list[soup_word] = cls.__build_words(dto['words'])
        panel: list[list[soup_position]] = cls.__build__from_resume_panel(dto['panel'])
        return soup_panel(panel, words)
    
    @classmethod
    def build_from_dto(cls, dto: Any) -> soup_panel:
        words: list[soup_word] = cls.__build_words(dto['words'])
        panel: list[list[soup_position]] = cls.__build_from_panel(dto['panel'])
        return soup_panel(panel, words)
    
    @classmethod
    def __build_words(cls, dtos: list[Any]) -> list[soup_word]:
        words: list[soup_word] = []
        for dto in dtos:
            word: soup_word = cls.__build_word(dto)
            words.append(word)
        return words
    
    @classmethod
    def __build_word(cls, dto: Any) -> list[soup_word]:
        characters:  dict[soup_character] = cls.__build_characters(dto['characters'])
        orientation: str = dto['orientation']
        word: str = dto['word']
        resolved: bool = dto.get('resolved')
        if resolved is None:
            resolved = False
        return soup_word(characters, orientation, word, resolved)
    
    @classmethod
    def __build_characters(cls, dtos: list[Any]) -> dict[soup_character]:
        characters: dict[soup_character] = {}
        for dto in dtos:
            character: soup_character = cls.__build_character(dtos[dto])
            characters[character.key()] = character
        return characters
    
    @classmethod
    def __build_character(cls, dto: Any) -> list[soup_character]:
        return soup_character(dto['character'], dto['x'], dto['y'])
    
    @classmethod
    def __build__from_resume_panel(cls, dtos: list[list[Any]]) -> list[list[soup_position]]:
        panel: list[list[soup_position]] = []
        for i_x, row in enumerate(dtos):
            panel_row: list[soup_position] = []
            for i_y, position in enumerate(row):
                character = position
                if position is " ":
                    character = "$"
                key: str = character + "-" + str(i_y) + "-" + str(i_x)
                position: soup_position = soup_position(key, character, False)
                panel_row.append(position)
            panel.append(panel_row)
        return panel
    
    @classmethod
    def __build_from_panel(cls, dtos: list[list[Any]]) -> list[list[soup_position]]:
        panel: list[list[soup_position]] = []
        for row in dtos:
            panel_row: list[soup_position] = []
            for position in row:
                position: soup_position = soup_position(position["identifier"], position["character"], position["resolved"])
                panel_row.append(position)
            panel.append(panel_row)
        return panel