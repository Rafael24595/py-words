from typing import Any


class ascii_gray_scale:
    
    __id: str
    __description: int
    
    def __init__(self, id: str, description: str) -> None:
        self.__id = id
        self.__description = description
        
    def as_dto(self) -> dict[str,Any]:
        return {"id": self.__id, "description": self.__description}