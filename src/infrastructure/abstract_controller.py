from abc import ABC

from fastapi import Request, Response
from commons.optional import optional
from commons.session.sessions import sessions

from infrastructure.py_petition import py_petition


class abstract_controller(ABC):
    
    def get_py_petition(self, request: Request, response: Response) -> py_petition:
        session_id: str = request.cookies.get("JSESSION_ID")
        sess = sessions.get_session(session_id)
        if(session_id is None or sess.is_none()):
            sess = optional.some(sessions.initialize())
            response.set_cookie("JSESSION_ID", sess.unwrap().get_id())
        return py_petition(sess, request, response)