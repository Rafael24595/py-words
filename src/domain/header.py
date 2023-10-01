class header():
    
    __key: str
    __value: str
    
    def __init__(self, key: str, value: str) -> None:
        self.__key = key
        self.__value = value
        
    def key(self) -> str:
        return self.__key
    
    def value(self) -> str:
        return self.__value