from domain.soup_panel.soup_character import soup_character

class soup_word:
    
    __characters: dict[str, soup_character]
    __orientation: str
    __word: str
    
    def __init__(self, characters: dict[str, soup_character], orientation: str, word: str) -> None:
        self.__characters = characters
        self.__orientation = orientation
        self.__word = word
        
    def characters(self) -> dict[str, soup_character]:
        return self.__characters
    
    def orientation(self) -> str:
        return self.__orientation
    
    def word(self) -> str:
        return self.__word