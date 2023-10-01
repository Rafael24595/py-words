from fastapi.templating import Jinja2Templates

from commons.configuration.dependency.dependency_container import dependency_container
from domain.soup import soup
from domain.soup_panel.soup_panel import soup_panel

from infrastructure.app.builder.module.clean_soup_actions import clean_soup_actions
from infrastructure.app.builder.module.ui_builder_module_app import ui_builder_module_app
from infrastructure.petition.i_py_petition import i_py_petition

class ui_builder_clean_soup(ui_builder_module_app):
    
    _templates = Jinja2Templates
    
    def __init__(self) -> None:
        self._templates = Jinja2Templates(directory="assets/app/" + clean_soup_actions.APP.value)
    
    async def build(self, petition: i_py_petition):
        container: dependency_container = dependency_container.instance()
        i_soup: soup = container.get_soup().unwrap()
        panel: soup_panel = await i_soup.generate_soup()
        context = {
            'request': petition.get_request(),
            'panel': panel.panel()
        }
        template = self._templates.TemplateResponse("index.html", context=context)
        petition.add_context(template)
    
    async def execute(self, action: str, petition: i_py_petition):
        pass