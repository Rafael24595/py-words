import os
from commons.configuration.dependency.dependency_container import dependency_container
from commons.configuration.dependency.dependency_dictionary import dependency_dictionary
from domain.dictionary import dictionary
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
        cache_instance: dictionary = dependency_dictionary.find_cache(args["SERVICE_CACHE"], args)
        dictionary_instance: dictionary = dependency_dictionary.find_dictionary(args["SERVICE_DICIONARY"], args)
        soup_instance: dictionary = dependency_dictionary.find_soup(args["SERVICE_SOUP"], args)
        dc.set_cache(cache_instance)
        dc.set_dictionary(dictionary_instance)
        dc.set_soup(soup_instance)