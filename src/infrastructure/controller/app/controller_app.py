from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from infrastructure.controller.abstract_controller import abstract_controller
from infrastructure.controller.app.builder.ui_builder_app import ui_builder_app
from infrastructure.controller.index.builder.ui_builder_index import ui_builder_index
from infrastructure.petition.i_py_petition import i_py_petition
BASE: str = "app"

class controller_app(abstract_controller):

    __router: APIRouter

    def __init__(self):
        self.__router = APIRouter(
            prefix="/" + BASE,
            tags=[BASE],
            responses={
                404: {"description": "Source not found"}
            },
        )
        self.__router.add_api_route("/{code}", self._load_app, methods=["GET"], response_class=HTMLResponse)
        self.__router.add_api_route("/{code}/{action}", self._execute, methods=["POST"], response_class=HTMLResponse)
        self.__router.add_api_route("/{code}/{action}", self._execute, methods=["GET"], response_class=HTMLResponse)
        
    def router(self) -> APIRouter:
        return self.__router
        
    async def _load_app(self, request: Request):
        petition: i_py_petition = self.request_to_py_petition(request)
        if request.headers.get("hx-request") != None:
            await ui_builder_app.build(petition)
        else:
            ui_builder_index.build(petition)
        return petition.get_response()
    
    async def _execute(self, request: Request):
        petition: i_py_petition = self.request_to_py_petition(request)
        if request.headers.get("hx-request") != None:
            await ui_builder_app.execute(petition)
        else:
            ui_builder_index.build(petition)
        return petition.get_response()