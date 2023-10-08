from typing import Any
import requests

from domain.dictionary import dictionary
from domain.permutation import permutation

class dictionary_app(dictionary):
    
    NAME: str = "dictionary_app"
    COMBO_LENGTH: int = 5
    COMBO_MIN: int = 4
    WORD_MIN: int = 4
    
    __connection: str
    
    def __init__(self, args: dict[str, str]) -> None:
        self.__connection = args["SERVICE_DICIONARY_CONNECTION"]
    
    async def generate_permutation(self) -> permutation:
        response = requests.get(self.__connection + "collection/permute?" + self.__get_query())
        json: dict[str,Any] = response.json()
        query: str = json["query"]
        words: list[str] = []
        for word in json["result"]:
            words.append(word["word"].upper())
        return permutation(query.upper(), words) 
    
    async def generate_target_permutation(self, target: str) -> permutation:
        return permutation(target, ["CALCULATE"]) 
    
    async def find_random(self, count: int) -> list[str]:
        return super().find_random(count)
        
    def __get_query(self) -> str:
        return "?combolen=" + str(dictionary_app.COMBO_LENGTH) + "&combomin=" + str(dictionary_app.COMBO_MIN) + "&min=" + str(dictionary_app.WORD_MIN) + "&exists=true"