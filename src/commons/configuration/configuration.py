from commons.Optional import Optional
from .ls_configuration.ls_configuration import ls_configuration

class configuration():
    
    singleton: 'Optional[configuration]' = Optional.none()
    
    left_sidebar: ls_configuration
    
    @classmethod
    def intitilaize(cls) -> 'configuration':
        if cls.singleton.is_some():
            raise Exception("Configuration already initialized.")
        cls.singleton = Optional.some(configuration())
        return cls.singleton.unwrap()
    
    @classmethod
    def instance(cls) -> 'configuration':
        if cls.singleton.is_none():
            raise Exception("Configuration not initialized.")
        return cls.singleton.unwrap()