from domain.dictionary import dictionary
from infrastructure.dictionary_memory import dictionary_memory

class dependency_dictionary():
    
    @classmethod
    def find_dictionary(*args: str) -> dictionary:
        return dictionary_memory(args)