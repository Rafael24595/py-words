from fastapi import Request, Response

from infrastructure.petition.py_petition import py_petition
from infrastructure.petition.py_petition_parser import py_petition_parser

class fastapi_petition_parser(py_petition_parser):
    
    __request: Request
    
    def __init__(self, request: Request) -> None:
        self.__request = request
    
    def get_request(self) -> Request:
        return self.__request
    
    def add_context(self, petition: py_petition, response: Response):
        petition.set_status(response.status_code)
        for header in response.raw_headers:
            petition.add_header(header[0].decode(), header[1].decode())
        petition.set_body(response.body.decode())
        petition.set_charset(response.charset)
        petition.set_media_type(response.media_type)
    
    def py_petition_to_response(self, petition: py_petition) -> Response:
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