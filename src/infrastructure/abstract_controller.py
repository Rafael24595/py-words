from abc import ABC

from fastapi import Request
from commons.optional import optional
from commons.session.sessions import sessions
from infrastructure.petition.parser.fastapi_petition_parser import fastapi_petition_parser
from infrastructure.petition.py_petition import py_petition

class abstract_controller(ABC):
    
    def request_to_py_petition(self, request: Request) -> py_petition:
        session_id: str = request.cookies.get("JSESSION_ID")
        sess = sessions.get_session(session_id)
        parser = fastapi_petition_parser(request)
        is_logged = True
        if(session_id is None or sess.is_none()):
            sess = optional.some(sessions.initialize())
            is_logged = False
        petition = py_petition(sess, parser)
        if not is_logged:
            petition.add_cookie("JSESSION_ID", sess.unwrap().get_id())
        return petition