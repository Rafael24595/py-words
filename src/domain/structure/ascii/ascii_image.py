from typing import Any

class ascii_image:
    
    __name: str
    __extension: int
    __height: int
    __width: int
    __status: str
    __message: str
    __frames: list[str]
    
    def __init__(self, name: str, extension: str, height: int, width: int, status: str, 
        message: str, frames: list[str]) -> None:
        self.__name = name
        self.__extension = extension
        self.__height = height
        self.__width = width
        self.__status = status
        self.__message = message
        self.__frames = frames
        
    def name(self) -> int:
        return self.__name
        
    def is_animation(self) -> int:
        return len(self.__frames) > 1
        
    def as_dto(self) -> dict[str,Any]:
        return {"name": self.__name, "extension": self.__extension, "height": self.__height,
                "width": self.__width, "status": self.__status, "message": self.__message,
                "frames": self.__frames}