class soup_config_param():
    
    __height: int
    __width: int
    __geometry: str
    
    def __init__(self, height: int, width: int, geometry: str) -> None:
        self.__height = height
        self.__width = width
        self.__geometry = geometry
        
    def height(self) -> int:
        return self.__height
    
    def width(self) -> int:
        return self.__width
    
    def geometry(self) -> int:
        return self.__geometry