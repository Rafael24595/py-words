from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from infrastructure.app.builder.ui_builder_app import ui_builder_app
from infrastructure.index.builder.ui_builder_index import ui_builder_index

BASE: str = "app"

class controller_app():

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
        
    def router(self) -> APIRouter:
        return self.__router
        
    async def _load_app(self, request: Request, code: str):
        if request.headers.get("hx-request") != None:
            return await ui_builder_app.build(code, request)
        return ui_builder_index.build(request)
    
    async def _execute(self, request: Request, code: str, action: str):
        if request.headers.get("hx-request") != None:
            return await ui_builder_app.execute(code, action, request)
        return ui_builder_index.build(request)
        