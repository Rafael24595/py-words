import requests
from domain.builder.soup_builder import soup_builder

from domain.soup import soup
from domain.soup_panel.soup_panel import soup_panel

class soup_app(soup):
    
    NAME: str = "soup_app"
    
    __connection: str
    __word_connection: str
    
    def __init__(self, args: dict[str, str]) -> None:
        self.__connection = args["SERVICE_SOUP_CONNECTION"]
        self.__word_connection = args["SERVICE_SOUP_CONNECTION_WORD"]
        
    def get_word_connection(self) -> str:
        return self.__word_connection
    
    async def generate_soup(self, configuration: str) -> soup_panel:
        dto = await self.__get_panel(configuration)
        panel = soup_builder.build_from_resume_dto(dto[0])
        return panel
    
    async def __get_panel(self, configuration: str): 
        response = requests.post(self.__connection + "api/1/soup-panel", data=configuration)
        return response.json()