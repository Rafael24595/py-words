from typing import Any
from fastapi.templating import Jinja2Templates

from commons.configuration.dependency.dependency_container import dependency_container
from domain.ascii_form import ascii_form
from domain.ascii_image import ascii_image
from domain.ascii import ascii

from infrastructure.app.builder.module.go_ascii_actions import go_ascii_actions
from infrastructure.app.builder.module.go_ascii_components import goa_ascii_components
from infrastructure.app.builder.module.ui_builder_module_app import ui_builder_module_app
from infrastructure.petition.i_py_petition import i_py_petition

class ui_builder_go_ascii(ui_builder_module_app):
    
    _templates = Jinja2Templates
    
    def __init__(self) -> None:
        self._templates = Jinja2Templates(directory="assets/app/" + go_ascii_actions.APP.value)
    
    async def build(self, petition: i_py_petition):
        return await self.__index(petition)
    
    async def execute(self, action: str, petition: i_py_petition):
        match(action):
            case go_ascii_actions.FORM.value:
                return await self.__form(petition)
            case go_ascii_actions.FIND.value:
                return await self.__take(petition)
            case go_ascii_actions.GENERATE.value:
                return await self.__generate(petition)
        return None
    
    async def __index(self, petition: i_py_petition):
        images = await self.__take_all_dict(petition)
        context = {
            'request': petition.get_request(),
            'app': go_ascii_actions.APP.value,
            'images': images,
            'action_find': go_ascii_actions.FIND.value,
            'action_form': go_ascii_actions.FORM.value,
        }
        template = self._templates.TemplateResponse(goa_ascii_components.INDEX.value, context=context)
        petition.add_context(template)
    
    async def __form(self, petition: i_py_petition):
        images = await self.__take_all_dict(petition)
        context = {
            'request': petition.get_request(),
            'app': go_ascii_actions.APP.value,
            'images': images,
            'action_generate': go_ascii_actions.GENERATE.value,
        }
        template = self._templates.TemplateResponse(goa_ascii_components.FORM.value, context=context)
        petition.add_context(template)
        
    async def __take_all_dict(self, petition: i_py_petition) -> list[dict[str,Any]]:
        container: dependency_container = dependency_container.instance()
        i_ascii: ascii = container.get_ascii().unwrap()
        dtos: list[dict[str,Any]] = []
        for item in await i_ascii.takeAll(): 
            dtos.append(item.as_dto())
        return dtos
    
    async def __generate(self, petition: i_py_petition):
        container: dependency_container = dependency_container.instance()
        i_ascii: ascii = container.get_ascii().unwrap()
        form = await self.__build_ascii_form(petition)
        image = await i_ascii.generate_ascii(form)
        await self.__build(petition, image)
        
    async def __take(self, petition: i_py_petition):
        container: dependency_container = dependency_container.instance()
        i_ascii: ascii = container.get_ascii().unwrap()
        key = petition.input_param_query("key")
        image = await i_ascii.take(key.unwrap())
        await self.__build(petition, image)
        
    async def __build_ascii_form(self, petition: i_py_petition) -> ascii_form:
        body: dict[str,Any] = await petition.input_json()
        code = body.get("code")
        height = body.get("height")
        width = body.get("width")
        sw_width_fix = body.get("sw_width_fix")
        gray_scale = body.get("gray_scale")
        image = body.get("image")
        return ascii_form(code, height, width, sw_width_fix, gray_scale, image)
        
    async def __build(self, petition: i_py_petition, image: ascii_image):
        dto = image.as_dto()
        context = {
            'request': petition.get_request(),
            'app': go_ascii_actions.APP.value, 
            'image': dto,
            'delay': 150
        }
        template: str = goa_ascii_components.IMAGE_STATIC.value
        if image.is_animation():
            template = goa_ascii_components.IMAGE_ANIMATE.value
        template = self._templates.TemplateResponse(template, context=context)
        petition.add_context(template)