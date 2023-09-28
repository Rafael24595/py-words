from fastapi.templating import Jinja2Templates

from fastapi import Request, Response
from commons.configuration.dependency.dependency_container import dependency_container
from commons.session.session import session
from commons.session.sessions import sessions
from domain.soup import soup
from domain.soup_panel.soup_panel import soup_panel

from infrastructure.app.builder.module.clean_soup_actions import clean_soup_actions
from infrastructure.app.builder.module.ui_builder_module_app import ui_builder_module_app

class ui_builder_clean_soup(ui_builder_module_app):
    
    _templates = Jinja2Templates
    
    def __init__(self) -> None:
        self._templates = Jinja2Templates(directory="assets/app/" + clean_soup_actions.APP.value)
    
    async def build(self, request: Request, response: Response):
        container: dependency_container = dependency_container.instance()
        i_soup: soup = container.get_soup().unwrap()
        panel: soup_panel = await i_soup.generate_soup()
        
        context = {
            'request': request,
            'panel': panel.panel()
        }
        
        return self._templates.TemplateResponse("index.html", headers=response.headers, context=context)
    
    async def execute(self, request: Request, response: Response):
        pass