from abc import ABC, abstractmethod

from domain.soup_panel.soup_panel import soup_panel

class soup(ABC):

    @abstractmethod
    async def generate_soup(self, configuration: str) -> soup_panel:
        pass