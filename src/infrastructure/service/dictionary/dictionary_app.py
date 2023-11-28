from typing import Any
import requests

from domain.dictionary import dictionary
from domain.structure.dictionary.permutation import permutation

class dictionary_app(dictionary):
    
    NAME: str = "dictionary_app"
    COMBO_LENGTH: int = 4
    COMBO_MIN: int = 4
    WORD_MIN: int = 4
    
    __connection: str
    
    def __init__(self, args: dict[str, str]) -> None:
        self.__connection = args["SERVICE_DICIONARY_CONNECTION"]
    
    async def generate_permutation(self, combolen: int) -> permutation:
        response = requests.get(self.__connection + "collection/permute?" + self.__get_query_without_combo(combolen))
        json: dict[str,Any] = response.json()
        combo: str = json["query"]
        words: list[str] = self.__get_words(json["result"])
        return permutation(combo.upper(), words) 
    
    async def generate_target_permutation(self, combo: str) -> permutation:
        response = requests.get(self.__connection + "collection/permute/" + combo + "?" + self.__get_query())
        json: dict[str,Any] = response.json()
        words: list[str] = self.__get_words(json["result"])
        return permutation(combo, words) 
    
    def __get_words(self, json: list[Any]) -> permutation:
        words: list[str] = []
        for word in json:
            words.append(word["word"].upper())
        return words 
    
    async def find_random(self, count: int) -> list[str]:
        response = requests.get(self.__connection + "collection/random?size=" + str(count))
        json: dict[str,Any] = response.json()
        return self.__get_words(json["result"])
        
    def __get_query(self, combolen: int) -> str:
        if combolen is None or combolen < 1:
            combolen = dictionary_app.COMBO_LENGTH
        return "min=" + str(dictionary_app.WORD_MIN) + "&exists=true"
        
    def __get_query_without_combo(self, combolen: int) -> str:
        if combolen is None or combolen < 1:
            combolen = 4
        return "combolen=" + str(combolen) + "&combomin=" + str(dictionary_app.COMBO_MIN) + "&min=" + str(dictionary_app.WORD_MIN) + "&exists=true"