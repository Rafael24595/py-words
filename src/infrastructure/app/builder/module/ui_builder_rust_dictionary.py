from fastapi.templating import Jinja2Templates

from fastapi import Request

from commons.configuration.dependency.dependency_container import dependency_container
from commons.optional import optional
from domain.cache import cache
from domain.dictionary import dictionary
from domain.permutation import permutation
from infrastructure.app.builder.module.ui_builder_module_app import ui_builder_module_app

BASE: str = "rust-dictionary"

class ui_builder_rust_dictionary(ui_builder_module_app):
    
    _templates = Jinja2Templates
    
    def __init__(self) -> None:
        self._templates = Jinja2Templates(directory="assets/app/" + BASE)

    async def build(self, request: Request):
        container: dependency_container = dependency_container.instance()
        i_dictionary: dictionary = container.get_dictionary().unwrap()
        i_cache: cache = container.get_cache().unwrap()
        i_permutation: permutation = await i_dictionary.generate_permutation()
        await i_cache.put(i_permutation.key(), i_permutation.struct())
        context = { 'request': request, 'base': BASE, 'action': 'result', 'reference': i_permutation.key(), 'permutation': i_permutation.get_base() }
        return self._templates.TemplateResponse("index.html", context)

    async def execute(self, action: str, request: Request):
        return await self._get_result(request)
    
    async def _get_result(self, request: Request):
        container: dependency_container = dependency_container.instance()
        body = await request.json()
        i_cache: cache = container.get_cache().unwrap()
        cached: optional[str] = await i_cache.get(body["reference"])
        if cached.is_some():
            return str(cached.unwrap())
        i_dictionary: dictionary = container.get_dictionary().unwrap()
        i_permutation: permutation = await i_dictionary.generate_permutation()
        return "Not cached! -> " + str(i_permutation.struct())