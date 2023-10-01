from typing import Any
from commons.constants.k_cookie import k_cookie
from commons.optional import optional
from commons.session.session import session
from domain.cookie import cookie
from domain.header import header
from infrastructure.petition.i_py_petition import i_py_petition
from infrastructure.petition.py_petition_parser import py_petition_parser

class py_petition(i_py_petition):
    
    __session: session
    __parser: py_petition_parser
    __status: int
    __media_type: str
    __charset: str
    __headers: dict[str,list[header]]
    __cookies: dict[str,list[cookie]]
    __body: Any
    __parameters: dict[str,Any]
    
    def __init__(self, sess: session, parser: py_petition_parser) -> None:
        self.__session = sess
        self.__parser = parser
        self.__status = 200
        self.__charset = "utf-8"
        self.__media_type = "text/html"
        self.__headers = {}
        self.__cookies = {}
        self.__body = ""
        self.__parameters = {}
        
    def get_session(self) -> session:
        return self.__session
    
    def get_request(self):
        return self.__parser.get_request()
    
    async def input_json(self) -> dict[str,Any]:
        return await self.__parser.input_json()
    
    def input_params_query(self) -> dict[str,str]:
        return self.__parser.input_params_query()
    
    def input_param_query(self, key: str) -> optional[str]:
        return self.__parser.input_param_query(key)
    
    def input_params_path(self) -> dict[str,str]:
        return self.__parser.input_params_path()
    
    def input_param_path(self, key: str) -> optional[str]:
        return self.__parser.input_param_path(key)
    
    def get_status(self) -> int:
        return self.__status
    
    def get_charset(self) -> str:
        return self.__charset
    
    def get_media_type(self) -> str:
        return self.__media_type
    
    def get_headers(self) -> dict[str,list[header]]:
        return self.__headers
    
    def get_cookies(self) -> dict[str,list[cookie]]:
        return self.__cookies
    
    def get_body(self) -> str:
        return self.__body
    
    def get_parameter(self, key: str) -> optional[Any]:
        return optional.some(self.__parameters.get(key))
    
    def set_status(self, status: int):
        self.__status = status
    
    def set_charset(self, charset: str) -> str:
        self.__charset = charset
    
    def set_media_type(self, media_type: str) -> str:
        self.__media_type = media_type
    
    def add_cookie(self, key: str, value: str, max_age: optional[int] = optional.none(), expires: optional[int] = optional.none(), 
        path: optional[str] = optional.none(), domain: optional[str] = optional.none(), secure: optional[bool] = optional.none(),
        httponly: optional[bool] = optional.none(), samesite: optional[k_cookie.k_same_site] = optional.none()) -> None:
        o_cookie = cookie(key, value, max_age, expires, path, domain, secure, httponly, samesite)
        if self.__cookies.get(key) is None:
            self.__cookies[key] = []
        self.__cookies[key].append(o_cookie)
    
    def add_header(self, key: str, value: str):
        o_header = header(key, value)
        if self.__headers.get(key) is None:
            self.__headers[key] = []
        self.__headers[key].append(o_header)
    
    def set_body(self, body: Any):
        self.__body = body
        
    def add_parameter(self, key: str, value: Any):
        self.__parameters[key] = value
        
    def add_context(self, response: Any):
        return self.__parser.add_context(self, response)
    
    def get_response(self):
        return self.__parser.py_petition_to_response(self)