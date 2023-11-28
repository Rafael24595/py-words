import datetime
from commons.constants.k_cookie import k_cookie
from commons.optional import optional

class cookie():
    
    __key: str
    __value: str
    __max_age: optional[int]
    __expires: optional[int]
    __path: optional[str]
    __domain: optional[str]
    __secure: optional[bool]
    __httponly: optional[bool]
    __samesite: optional[k_cookie.k_same_site]
    
    def __init__(self, key: str, value: str, max_age: optional[int], expires: optional[int], 
        path: optional[str], domain: optional[str], secure: optional[bool],
        httponly: optional[bool], samesite: optional[k_cookie.k_same_site]) -> None:
        self.__key = key
        self.__value = value
        self.__max_age = max_age
        self.__expires = expires
        self.__path = path
        self.__domain = domain
        self.__secure = secure        
        self.__httponly = httponly
        self.__samesite = samesite

    def as_chain(self):
        chain = self.__key + "=" + self.__value
        if self.__max_age.is_some():
            chain = chain + "; max-age=" + str(self.__max_age.unwrap())
        if self.__expires.is_some():
            chain = chain + "; expires=" + str(datetime.datetime.fromtimestamp(self.__max_age.unwrap()/1000.0))
        if self.__path.is_some():
            chain = chain + "; path=" + self.__path.unwrap()
        if self.__domain.is_some():
            chain = chain + "; domain=" + self.__domain.unwrap()
        if self.__secure.is_some():
            chain = chain + "; secure=" + str(self.__secure.unwrap())
        if self.__httponly.is_some():
            chain = chain + "; httponly=" + str(self.__httponly.unwrap())
        if self.__samesite.is_some():
            chain = chain + "; samesite=" + str(self.__samesite.unwrap())
        return chain