from abc import ABC, abstractmethod

from fastapi import Request, Response

class ui_builder_module_app(ABC):

    @abstractmethod
    async def build(self, request: Request, response: Response):
        pass

    @abstractmethod
    async def execute(self, action: str, request: Request, response: Response):
        pass