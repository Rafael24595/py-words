from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from index.infrastructure.controller_index import controller_index

class controller_app():

    _base: controller_index
    _templates = Jinja2Templates(directory="assets/app")

    def __init__(self, base: controller_index):
        self._base = base
        router: APIRouter = self._base.router()
        router.add_api_route("/app/{code}", self._load_app, methods=["GET"], response_class=HTMLResponse)
        
    async def _load_app(self, request: Request, code: str):
        if request.headers.get("hx-request") != None:
            return "<h1>" + code + "</h1>"
        return await self._base._load_index(request)
        