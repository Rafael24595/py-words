from .configuration import configuration
from .ls_configuration.ls_configuration import ls_configuration

class configurator():
    
    @classmethod
    def initialize(cls) -> 'configurator':
        conf = configuration.intitilaize()
        conf.left_sidebar = ls_configuration.instance()