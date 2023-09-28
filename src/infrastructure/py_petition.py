from fastapi import Request, Response
from commons.session.session import session


class py_petition():
    
    __session: session
    __request: Request
    __response: Response
    
    def __init__(self, sess: session, request: Request, response: Response) -> None:
        self.__session = sess
        self.__request = request
        self.__response = response
        
    def get_session(self) -> session:
        return self.__session
    
    def get_request(self) -> Request:
        self.__request
    
    def get_response(self) -> Response:
        return self.__response
    