from typing import TypeVar, Generic, List

T = TypeVar('T')

class optional(Generic[T]):
    
    _element: T
    
    def __init__(self, element: T) -> None:
        self._element = element
    
    @classmethod
    def some(cls, element: T) -> 'optional[T]':
        return optional(element)
    
    @classmethod
    def none(cls) -> 'optional[T]':
        return optional(None)
    
    def is_some(self) -> bool:
        return self._element != None
    
    def is_none(self) -> bool:
        return not self.is_some()
    
    def unwrap(self):
        if self._element != None:
            return self._element
        raise Exception('Cannot unwrap a None element.')