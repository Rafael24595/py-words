from abc import ABC, abstractmethod

from domain.structure.soup.soup_panel import soup_panel

class soup(ABC):

    @abstractmethod
    def get_word_connection(self) -> str:
        pass

    @abstractmethod
    async def generate_soup(self, configuration: str) -> soup_panel:
        pass