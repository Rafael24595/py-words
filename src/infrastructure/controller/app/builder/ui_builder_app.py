from commons.optional import optional
from infrastructure.controller.app.builder.module.ui_builder_go_ascii import ui_builder_go_ascii
from infrastructure.controller.app.builder.module.ui_builder_module_app import ui_builder_module_app
from infrastructure.controller.app.builder.module.ui_builder_clean_soup import ui_builder_clean_soup
from infrastructure.controller.app.builder.module.ui_builder_rust_dictionary import ui_builder_rust_dictionary
from infrastructure.controller.index.builder.ui_builder_index import ui_builder_index
from infrastructure.petition.i_py_petition import i_py_petition

class ui_builder_app():
        
    __ui_builder_clean_soup: ui_builder_clean_soup = ui_builder_clean_soup()
    __ui_builder_rust_dictionary: ui_builder_rust_dictionary = ui_builder_rust_dictionary()
    __ui_builder_go_ascii: ui_builder_go_ascii = ui_builder_go_ascii()
 
    @classmethod
    async def build(cls, petition: i_py_petition):
        return await cls._build_module(petition)
        
    @classmethod
    async def _build_module(cls, petition: i_py_petition):
        code: str = petition.input_param_path("code").unwrap()
        builder: optional[ui_builder_module_app] = cls._find_builder(code)
        if builder.is_some():
            return await builder.unwrap().build(petition)
        return ui_builder_index.build(petition)
    
    @classmethod
    async def execute(cls, petition: i_py_petition):
        code: str = petition.input_param_path("code").unwrap()
        action: str = petition.input_param_path("action").unwrap()
        builder: optional[ui_builder_module_app] = cls._find_builder(code)
        if builder.is_some():
            return await builder.unwrap().execute(action, petition)
        return ui_builder_index.build(petition)
    
    @classmethod
    def _find_builder(cls, code: str) -> optional[ui_builder_module_app]:
        match code:
            case "rust-dictionary":
                return optional.some(cls.__ui_builder_rust_dictionary)
            case "clean-soup":
                return optional.some(cls.__ui_builder_clean_soup)
            case "go-ascii":
                return optional.some(cls.__ui_builder_go_ascii)

        return optional.none()