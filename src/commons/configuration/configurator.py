from commons.configuration.dependency.dependency_container import dependency_container
from commons.configuration.dependency.dependency_dictionary import dependency_dictionary
from domain.dictionary import dictionary
from .configuration import configuration
from .ls_configuration.ls_configuration import ls_configuration

class configurator():
    
    @classmethod
    def initialize(cls) -> 'configurator':
        conf = configuration.intitilaize()
        conf.left_sidebar = ls_configuration.instance()
        cls._define_dependencies()
        
    @classmethod
    def _define_dependencies(cls):
        dc: dependency_container = dependency_container.instance()
        dictionary_instance: dictionary = dependency_dictionary.find_dictionary(None)
        dc.set_dictionary(dictionary_instance)