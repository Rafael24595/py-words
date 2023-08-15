from fastapi.templating import Jinja2Templates

from fastapi import Request

from infrastructure.app.builder.module.ui_builder_module_app import ui_builder_module_app

BASE: str = "clean-soup"

class ui_builder_clean_soup(ui_builder_module_app):
    
    _templates = Jinja2Templates
    
    def __init__(self) -> None:
        self._templates = Jinja2Templates(directory="assets/app/" + BASE)
    
    async def build(self, request: Request):
        return "<h1>" + BASE + "</h1>"
    
    async def execute(self, request: Request):
        pass