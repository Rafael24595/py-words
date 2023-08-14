from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from commons.configuration.configuration import configuration

BASE: str = "index"

class controller_index():

    __router: APIRouter
    _templates = Jinja2Templates(directory="assets/" + BASE)

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
        conf: configuration = configuration.instance()
        headers = []
        footers = []
        ls_conf = conf.left_sidebar
        body = {
            'ls_sidebar': {
                "title": ls_conf.title(),
                "elements": ls_conf.json_elements()
            }
        }
        context = { 'request': request, 'base': BASE, 'headers': headers, 'body': body, 'footers': footers }
        return self._templates.TemplateResponse("index.html", context)