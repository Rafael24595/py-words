from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

class controller_index():

    __router: APIRouter
    _templates = Jinja2Templates(directory="src/assets/index")

    def __init__(self):
        self.__router = APIRouter(
            prefix="/index",
            tags=["index"],
            responses={
                404: {"description": "Source not found"}
            },
        )

        self.__router.add_api_route("/", self._load_index, methods=["GET"], response_class=HTMLResponse)
        
    def get_router(self) -> APIRouter:
        return self.__router
        
    async def _load_index(self, request: Request):
        headers = []
        footers = []
        ls_elements = []
        body = {
            'ls_elements': ls_elements   
        }
        context = { 'request': request, 'headers': headers, 'body': body, 'footers': footers }
        return self._templates.TemplateResponse("index.html", context)