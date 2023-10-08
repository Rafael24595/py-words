from typing import Any
from fastapi.templating import Jinja2Templates

from commons.configuration.dependency.dependency_container import dependency_container
from domain.builder.soup_builder import soup_builder
from domain.builder.soup_config_builder import soup_config_builder
from domain.dictionary import dictionary
from domain.soup import soup
from domain.soup_panel.soup_character import soup_character
from domain.soup_panel.soup_config_param import soup_config_param
from domain.soup_panel.soup_panel import soup_panel

from infrastructure.app.builder.module.clean_soup_actions import clean_soup_actions
from infrastructure.app.builder.module.ui_builder_module_app import ui_builder_module_app
from infrastructure.petition.i_py_petition import i_py_petition

class ui_builder_clean_soup(ui_builder_module_app):
    
    _templates = Jinja2Templates
    
    def __init__(self) -> None:
        self._templates = Jinja2Templates(directory="assets/app/" + clean_soup_actions.APP.value)
    
    async def build(self, petition: i_py_petition):
        return await self.__form(petition)
    
    async def execute(self, action: str, petition: i_py_petition):
        match(action):
            case clean_soup_actions.FORM.value:
                return await self.__form(petition)
            case clean_soup_actions.PANEL.value:
                return await self.__panel(petition)
            case clean_soup_actions.RESOLVE.value:
                return await self.__resolve(petition)
        return None
    
    async def __form(self, petition: i_py_petition):
        context = {
            'request': petition.get_request(),
            'app': clean_soup_actions.APP.value, 
            'action_panel': clean_soup_actions.PANEL.value,
        }
        template = self._templates.TemplateResponse("index.html", context=context)
        petition.add_context(template)
    
    async def __panel(self, petition: i_py_petition):
        container: dependency_container = dependency_container.instance()
        i_soup: soup = container.get_soup().unwrap()
        i_dictionary: dictionary = container.get_dictionary().unwrap()
        configuration: str = await self.__build_config_parameters(petition)
        panel: soup_panel = await i_soup.generate_soup(configuration)
        words: list[str] = await i_dictionary.find_random(2)
        name = words[0] + " " + words[1]
        await self.__build(petition, name, panel)
        
    async def __build_config_parameters(self, petition: i_py_petition):
        body: dict[str,Any] = await petition.input_json()
        height = body.get("height")
        width = body.get("width")
        geometry = body.get("geometry")
        geometry_range = body.get("geometry-range")
        params: soup_config_param = soup_config_param(height, width, geometry, geometry_range)
        return soup_config_builder.build(params)
        
    async def __resolve(self, petition: i_py_petition):
        dto = await petition.get_session().unstore(clean_soup_actions.APP.value)
        ##TODO: Uncontrolled optional unwrap.
        panel: soup_panel = soup_builder.build_from_dto(dto.unwrap().data())
        json = await petition.input_json()
        name = json["soup_name"]
        characters: list[soup_character] = []
        for raw_character in json.values():
            split = raw_character.split("-")
            ##TODO: Builder from string.
            if len(split) == 3:
                character = soup_character(split[0], split[1], split[2])
                characters.append(character)
        panel.check_characters(characters)
        await self.__build(petition, name, panel)
        
    async def __build(self, petition: i_py_petition, name: str, panel: soup_panel):
        words: list[str] = panel.words_status()
        dto = panel.as_dto()
        context = {
            'request': petition.get_request(),
            'app': clean_soup_actions.APP.value, 
            'action_resolve': clean_soup_actions.RESOLVE.value,
            'action_form': clean_soup_actions.FORM.value,
            'soup_name': name,
            'words': words,
            'panel': dto.get("panel"),
            'total': len(panel.words()),
            'resolved': len(panel.resolved_words())
        }
        await petition.get_session().store(clean_soup_actions.APP.value, dto)
        
        template = self._templates.TemplateResponse("panel.html", context=context)
        petition.add_context(template)