from abc import ABC, abstractmethod

from infrastructure.petition.i_py_petition import i_py_petition

class ui_builder_module_app(ABC):

    @abstractmethod
    async def build(self, petition: i_py_petition):
        pass

    @abstractmethod
    async def execute(self, action: str, petition: i_py_petition):
        pass