import json
from domain.structure.builder.soup_builder import soup_builder

from domain.soup import soup
from domain.structure.soup.soup_panel import soup_panel

class soup_memory(soup):
    
    NAME: str = "soup_memory"
    
    def __init__(self, args: dict[str, str]) -> None:
        pass
    
    def get_word_connection(self) -> str:
        return ""
    
    async def generate_soup(self, configuration: str) -> soup_panel:
        file = open('assets/test/soup_output.json')
        dto = json.load(file)
        panel = soup_builder.build_from_resume_dto(dto)
        file.close()
        return panel