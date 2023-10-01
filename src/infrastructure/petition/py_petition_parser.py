from abc import ABC, abstractmethod
from typing import Any

from infrastructure.petition.i_py_petition import i_py_petition

class py_petition_parser(ABC):
    
    @abstractmethod
    def get_request(self) -> Any:
        pass
    
    @abstractmethod
    def add_context(self, petition: i_py_petition, response: Any):
        pass
    
    @abstractmethod
    def py_petition_to_response(self, petition: i_py_petition) -> Any:
        pass