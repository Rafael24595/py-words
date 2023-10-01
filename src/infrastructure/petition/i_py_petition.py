from abc import ABC, abstractmethod
from typing import Any
from commons.constants.k_cookie import k_cookie
from commons.optional import optional
from commons.session.session import session
from domain.cookie import cookie
from domain.header import header

class i_py_petition(ABC):
        
    @abstractmethod
    def get_session(self) -> session:
        pass
    
    @abstractmethod
    def get_request(self):
        pass
    
    @abstractmethod
    async def input_json(self) -> dict[str,Any]:
        pass
    
    @abstractmethod
    def input_params_query(self) -> dict[str,str]:
        pass
    
    @abstractmethod
    def input_param_query(self, key: str) -> optional[str]:
        pass
    
    @abstractmethod
    def input_params_path(self) -> dict[str,str]:
        pass
    
    @abstractmethod
    def input_param_path(self, key: str) -> optional[str]:
        pass
    
    @abstractmethod
    def get_status(self) -> int:
        pass
    
    @abstractmethod
    def get_charset(self) -> str:
        pass
    
    @abstractmethod
    def get_media_type(self) -> str:
        pass
    
    @abstractmethod
    def get_headers(self) -> dict[str,list[header]]:
        pass
    
    @abstractmethod
    def get_cookies(self) -> dict[str,list[cookie]]:
        pass
    
    @abstractmethod
    def get_body(self) -> str:
        pass
    
    @abstractmethod
    def get_parameter(self, key: str) -> optional[Any]:
        pass
    
    @abstractmethod
    def set_status(self, status: int):
        pass
    
    @abstractmethod
    def set_charset(self, charset: str) -> str:
        pass
    
    @abstractmethod
    def set_media_type(self, media_type: str) -> str:
        pass
    
    @abstractmethod
    def add_cookie(self, key: str, value: str, max_age: optional[int] = optional.none(), expires: optional[int] = optional.none(), 
        path: optional[str] = optional.none(), domain: optional[str] = optional.none(), secure: optional[bool] = optional.none(),
        httponly: optional[bool] = optional.none(), samesite: optional[k_cookie.k_same_site] = optional.none()) -> None:
        pass
    
    @abstractmethod
    def add_header(self, key: str, value: str):
        pass
    
    @abstractmethod
    def set_body(self, body: Any):
        pass
        
    @abstractmethod
    def add_context(self, response: Any):
        pass
    
    @abstractmethod
    def add_parameter(self, key: str, value: Any):
        pass
    
    @abstractmethod
    def get_response(self):
        pass