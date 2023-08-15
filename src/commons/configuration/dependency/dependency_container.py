from commons.optional import optional
from domain.cache import cache
from domain.dictionary import dictionary

class dependency_container:
    
    singleton: 'optional[dependency_container]' = optional.none()
    
    _cache: optional[cache]
    _dictionary: optional[dictionary]
    
    def __init__(self) -> None:
        self._dictionary = optional.none()
    
    @classmethod
    def instance(cls) -> 'dependency_container':
        if cls.singleton.is_none():
            cls.singleton = optional.some(dependency_container())
        return cls.singleton.unwrap()
    
    def get_cache(self) -> optional[cache]:
        return self._cache
    
    def set_cache(self, instance: cache) -> None:
        self._cache = optional.some(instance)
    
    def get_dictionary(self) -> optional[dictionary]:
        return self._dictionary
    
    def set_dictionary(self, instance: dictionary) -> None:
        self._dictionary = optional.some(instance)