from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from infrastructure.app.builder.builder_app import builder_app
from infrastructure.index.builder.builder_index import builder_index

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
        
    def router(self) -> APIRouter:
        return self.__router
        
    async def _load_app(self, request: Request, code: str):
        if request.headers.get("hx-request") != None:
            return await builder_app.build(code, request)
        return builder_index.build(request)
        