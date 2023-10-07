class soup_config_param():
    
    __height: int
    __width: int
    __geometry: str
    __geometry_range: int
    
    def __init__(self, height: int, width: int, geometry: str, geometry_range: int) -> None:
        self.__height = height
        self.__width = width
        self.__geometry = geometry
        self.__geometry_range = geometry_range
        
    def height(self) -> int:
        return self.__height
    
    def width(self) -> int:
        return self.__width
    
    def geometry(self) -> str:
        return self.__geometry
    
    def geometry_range(self) -> int:
        return self.__geometry_range