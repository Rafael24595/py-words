from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from infrastructure.controller.abstract_controller import abstract_controller

from infrastructure.controller.index.builder.ui_builder_index import ui_builder_index
from infrastructure.petition.i_py_petition import i_py_petition

BASE: str = "index"

class controller_index(abstract_controller):

    __router: APIRouter

    def __init__(self):
        self.__router = APIRouter(
            prefix="/" + BASE,
            tags=[BASE],
            responses={
                404: {"description": "Source not found"}
            },
        )

        self.__router.add_api_route("", self._load_index, methods=["GET"], response_class=HTMLResponse)
        
    def router(self) -> APIRouter:
        return self.__router
        
    async def _load_index(self, request: Request):
        petition: i_py_petition = self.request_to_py_petition(request)
        ui_builder_index.build(petition)
        return petition.get_response()