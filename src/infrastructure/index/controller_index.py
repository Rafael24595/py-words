from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from infrastructure.index.builder.ui_builder_index import ui_builder_index

BASE: str = "index"

class controller_index():

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
        return ui_builder_index.build(request)