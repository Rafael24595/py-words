import threading
import uuid

from commons.optional import optional
from commons.session.session import session

class sessions():
    
    __lock: threading.Lock = threading.Lock()
    __sessions: dict[str, session] = {}
    
    @classmethod
    def initialize(cls) -> session:
        id: optional[str] = optional.none()
        while id.is_none() or cls.__exists(id.unwrap()):
            id = optional.some(str(uuid.uuid4()))
        sess = session(id.unwrap())
        return cls.__push_session(sess)
        
    @classmethod
    def __exists(cls, id: str):
        return cls.get_session(id).is_some()
        
    @classmethod
    def get_session(cls, id: str) -> optional[session]:
        session = cls.__sessions.get(id)
        if(session is None):
            return optional.none()
        return optional.some(session)
    
    @classmethod
    def __push_session(cls, sess: session) -> session:
        cls.__lock.acquire()
        cls.__sessions[sess.get_id()] = sess
        cls.__lock.release()
        return sess