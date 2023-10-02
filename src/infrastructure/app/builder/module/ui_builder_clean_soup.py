from fastapi.templating import Jinja2Templates

from commons.configuration.dependency.dependency_container import dependency_container
from domain.builder.soup_builder import soup_builder
from domain.soup import soup
from domain.soup_panel.soup_character import soup_character
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
        await self.__build(petition, panel)
    
    async def execute(self, action: str, petition: i_py_petition):
        match(action):
            case clean_soup_actions.RESOLVE.value:
                return await self.__resolve(petition)
        return None
    
    async def __resolve(self, petition: i_py_petition):
        dto = await petition.get_session().unstore(clean_soup_actions.APP.value)
        ##TODO: Uncontrolled optional unwrap.
        panel: soup_panel = soup_builder.build_from_dto(dto.unwrap().data())
        raw_characters = await petition.input_json()
        characters: list[soup_character] = []
        for raw_character in raw_characters.values():
            split = raw_character.split("-")
            ##TODO: Builder from string.
            character = soup_character(split[0], split[1], split[2])
            characters.append(character)
        panel.check_characters(characters)
        await self.__build(petition, panel)
        
    async def __build(self, petition: i_py_petition, panel: soup_panel):
        resolved: list[str] = panel.resolved_words()
        dto = panel.as_dto()
        context = {
            'request': petition.get_request(),
            'app': clean_soup_actions.APP.value, 
            'action_resolve': clean_soup_actions.RESOLVE.value,
            'resolved': resolved,
            'panel': dto.get("panel")
        }
        await petition.get_session().store(clean_soup_actions.APP.value, dto)
        
        template = self._templates.TemplateResponse("index.html", context=context)
        petition.add_context(template)