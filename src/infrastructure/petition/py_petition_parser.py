from abc import ABC, abstractmethod
from typing import Any
from commons.optional import optional

from infrastructure.petition.i_py_petition import i_py_petition

class py_petition_parser(ABC):
    
    @abstractmethod
    def get_request(self) -> Any:
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
    def add_context(self, petition: i_py_petition, response: Any):
        pass
    
    @abstractmethod
    def py_petition_to_response(self, petition: i_py_petition) -> Any:
        pass