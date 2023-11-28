import os
from commons.configuration.dependency.dependency_container import dependency_container
from commons.configuration.dependency.dependency_dictionary import dependency_dictionary
from domain.ascii_persistence import ascii_persistence
from domain.cache import cache
from domain.dictionary import dictionary
from domain.soup import soup
from domain.ascii import ascii
from .configuration import configuration
from .ls_configuration.ls_configuration import ls_configuration
from dotenv import load_dotenv

load_dotenv()

class configurator():
    
    @classmethod
    def initialize(cls) -> 'configurator':
        conf = configuration.intitilaize()
        conf.left_sidebar = ls_configuration.instance()
        args = cls.__load_env()
        cls._define_dependencies(args)
        
    @classmethod
    def __load_env(cls) -> dict[str, str]:
        args: dict[str,str] = {}
        for name, value in os.environ.items():
            args[name] = value
        return args
        
    @classmethod
    def _define_dependencies(cls, args: dict[str, str]):
        dc: dependency_container = dependency_container.instance()
        cache_instance: cache = dependency_dictionary.find_cache(args["SERVICE_CACHE"], args)
        dictionary_instance: dictionary = dependency_dictionary.find_dictionary(args["SERVICE_DICIONARY"], args)
        soup_instance: soup = dependency_dictionary.find_soup(args["SERVICE_SOUP"], args)
        ascii_instance: ascii = dependency_dictionary.find_ascii(args["SERVICE_ASCII"], args)
        ascii_persistence_instance: ascii_persistence = dependency_dictionary.find_ascii_persistence(args["SERVICE_ASCII_PERSISTENCE"], args)
        ascii_instance.enablePersistence(ascii_persistence_instance)
        dc.set_cache(cache_instance)
        dc.set_dictionary(dictionary_instance)
        dc.set_soup(soup_instance)
        dc.set_ascii(ascii_instance)