class ascii_form:
    
    __code: str
    __height: int
    __width: int
    __sw_width_fix: bool
    __gray_scale: str
    __image: str
    
    def __init__(self, code: str, height: int, width: int, sw_width_fix: bool, 
        gray_scale: str, image: str) -> None:
        self.__code = code
        self.__height = height
        self.__width = width
        self.__sw_width_fix = sw_width_fix
        self.__gray_scale = gray_scale
        self.__image = image
        
    def to_dict(self):
        return {"code": self.__code, "height": self.__height, "width": self.__width, 
            "sw_width_fix": self.__sw_width_fix, "gray_scale": self.__gray_scale, "image": self.__image}