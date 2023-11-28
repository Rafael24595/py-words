from domain.ascii_persistence import ascii_persistence
from domain.cache import cache
from domain.dictionary import dictionary
from domain.soup import soup
from domain.ascii import ascii
from infrastructure.ascii_app import ascii_app
from infrastructure.ascii_memory import ascii_memory
from infrastructure.ascii_persistence_memory import ascii_persistence_memory
from infrastructure.cache_memory import cache_memory
from infrastructure.dictionary_app import dictionary_app
from infrastructure.dictionary_memory import dictionary_memory
from infrastructure.soup_app import soup_app
from infrastructure.soup_memory import soup_memory

class dependency_dictionary():
    
    @classmethod
    def find_cache(cls, code: str, args: dict[str, str]) -> cache:
        match code:
            case cache_memory.NAME:
                return cache_memory(args)
        raise Exception("Cache service not found")
    
    @classmethod
    def find_dictionary(cls, code: str, args: dict[str, str]) -> dictionary:
        match code:
            case dictionary_memory.NAME:
                return dictionary_memory(args)
            case dictionary_app.NAME:
                return dictionary_app(args)
        raise Exception("Dictionary service not found")
        
    
    @classmethod
    def find_soup(cls, code: str, args: dict[str, str]) -> soup:
        match code:
            case soup_memory.NAME:
                return soup_memory(args)
            case soup_app.NAME:
                return soup_app(args)
        raise Exception("Dictionary service not found")
    
    @classmethod
    def find_ascii(cls, code: str, args: dict[str, str]) -> ascii:
        match code:
            case ascii_memory.NAME:
                return ascii_memory(args)
            case ascii_app.NAME:
                return ascii_app(args)
        raise Exception("Ascii service not found")
    
    @classmethod
    def find_ascii_persistence(cls, code: str, args: dict[str, str]) -> ascii_persistence:
        match code:
            case ascii_persistence_memory.NAME:
                return ascii_persistence_memory(args)
        raise Exception("Ascii persistence service not found")