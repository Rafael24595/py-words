from domain.cache import cache
from domain.dictionary import dictionary
from infrastructure.cache_memory import cache_memory
from infrastructure.dictionary_memory import dictionary_memory

class dependency_dictionary():
    
    @classmethod
    def find_cache(*args: str) -> cache:
        return cache_memory(args)
    
    @classmethod
    def find_dictionary(*args: str) -> dictionary:
        return dictionary_memory(args)