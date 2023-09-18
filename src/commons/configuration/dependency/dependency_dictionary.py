from domain.cache import cache
from domain.dictionary import dictionary
from domain.soup import soup
from infrastructure.cache_memory import cache_memory
from infrastructure.dictionary_memory import dictionary_memory
from infrastructure.soup_memory import soup_memory

class dependency_dictionary():
    
    @classmethod
    def find_cache(*args: str) -> cache:
        return cache_memory(args)
    
    @classmethod
    def find_dictionary(*args: str) -> dictionary:
        return dictionary_memory(args)
    
    @classmethod
    def find_soup(*args: str) -> soup:
        return soup_memory(args)