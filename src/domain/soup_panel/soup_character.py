class soup_character:
    
    __character: str
    __x: int
    __y: int
    
    def __init__(self, character: str, x: int, y: int) -> None:
        self.__character = character
        self.__x = x
        self.__y = y
        
    def character(self) -> str:
        return self.__character
    
    def x(self) -> int:
        return self.__x
    
    def y(self) -> int:
        return self.__y
    
    def key(self) -> str:
        return self.__character + "-" + str(self.__x) + "-" + str(self.__y)