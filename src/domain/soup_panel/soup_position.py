from typing import Any

class soup_position:
    
    __identifier: str
    __character: str
    __resolved: bool
    
    def __init__(self, identifier: str, character: str, resolved: bool) -> None:
        self.__identifier = identifier
        self.__character = character
        self.__resolved = resolved
        
    def identifier(self) -> str:
        return self.__identifier
        
    def character(self) -> str:
        return self.__character
    
    def is_resolved(self) -> bool:
        return self.__resolved
    
    def mark_as_resolved(self):
        self.__resolved = True
    
    def mark_as_unresolved(self):
        self.__resolved = False
    
    def as_dto(self) -> dict[str,Any]:
        dto: dict[str,Any] = {}
        dto["identifier"] = self.__identifier
        dto["character"] = self.__character
        dto["resolved"] = self.__resolved
        return dto