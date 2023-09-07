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