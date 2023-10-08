from typing import Any
from fastapi import Request, Response
from commons.optional import optional

from infrastructure.petition.i_py_petition import i_py_petition
from infrastructure.petition.py_petition_parser import py_petition_parser

class fastapi_petition_parser(py_petition_parser):
    
    __request: Request
    __params_query: dict[str,str]
    __params_path: dict[str,str]
    
    def __init__(self, request: Request) -> None:
        self.__request = request
        self.__load_params_query()
        self.__load_params_path()
        
    def __load_params_query(self):
        self.__params_query = {}
        for key in self.__request.query_params.keys():
            self.__params_query[key] = self.__request.query_params.get(key)
    
    def __load_params_path(self) -> dict[str,str]:
        self.__params_path = {}
        for key in self.__request.path_params.keys():
            self.__params_path[key] = self.__request.path_params.get(key)
    
    def get_request(self) -> Request:
        return self.__request
    
    async def input_json(self) -> dict[str,Any]:
        if (await self.__request.body()).decode() == "":
            return {}
        return await self.__request.json()
    
    def input_params_query(self) -> dict[str,str]:
        return self.__params_query
    
    def input_param_query(self, key: str) -> optional[str]:
        return optional.some(self.__params_query.get(key))
    
    def input_params_path(self) -> dict[str,str]:
        return self.__params_path
    
    def input_param_path(self, key: str) -> optional[str]:
        return optional.some(self.__params_path.get(key))
    
    def add_context(self, petition: i_py_petition, response: Response):
        petition.set_status(response.status_code)
        for header in response.raw_headers:
            petition.add_header(header[0].decode(), header[1].decode())
        petition.set_body(response.body.decode())
        petition.set_charset(response.charset)
        petition.set_media_type(response.media_type)
    
    def py_petition_to_response(self, petition: i_py_petition) -> Response:
        response = Response()
        
        response.raw_headers = []
        
        response.status_code = petition.get_status()
        response.charset = petition.get_charset()
        response.media_type = petition.get_media_type()
        
        headers = petition.get_headers()
        for key in headers:
            values = headers[key]
            for header in values:
                response.raw_headers.append((header.key().encode("latin-1"), header.value().encode("latin-1")))
                
        cookies = petition.get_cookies()
        for key in cookies:
            values = cookies[key]
            for cookie in values:
                response.raw_headers.append((b"set-cookie", cookie.as_chain().encode("latin-1")))
        
        response.body = petition.get_body().encode(petition.get_charset())
        
        return response