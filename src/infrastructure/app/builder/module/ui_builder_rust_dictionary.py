from typing import Any
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
        i_permutation: permutation = await self._generate_permutation()
        j_permutation = {
            'target': i_permutation.get_base(),
            'reference': i_permutation.key()
        }
        context = { 'request': request, 'base': BASE, 'action': 'result', 'permutation': j_permutation }
        return self._templates.TemplateResponse("index.html", context)

    async def execute(self, action: str, request: Request):
        match(action):
            case "result":
                return await self._build_result(request)
            case "add-word":
                return await self._build_added_words(request)
            case "remove-word":
                return await self._build_remove_words(request)
    
    async def _build_result(self, request: Request):
        body: Any = await request.json()
        i_permutation: permutation = await self._find_result(body)
        return str(i_permutation.struct())
    
    async def _build_added_words(self, request: Request):
        body: map[str,Any] = await request.json()
        added_words_raw = body.get('added-word')
        added_words = []
        if isinstance(added_words_raw, list):
            added_words = added_words_raw
        elif not added_words_raw == None:
            added_words = [added_words_raw]
        add_word_raw = body.get('add-word')
        words: list[str] = added_words
        if add_word_raw not in added_words and add_word_raw != None:
            words = [add_word_raw] + words
        context = { 'request': request, 'base': BASE, 'words':  words}
        return self._templates.TemplateResponse("added-word-container.html", context)
    
    async def _build_remove_words(self, request: Request):
        body: map[str,Any] = await request.json()
        word = request.query_params.get("word")
        added_words_raw = body.get('added-word')
        words = []
        if isinstance(added_words_raw, list):
            words = added_words_raw
        elif not added_words_raw == None:
            words = [added_words_raw]
        if word in words:
            words.remove(word)
        context = { 'request': request, 'base': BASE, 'words':  words}
        return self._templates.TemplateResponse("added-word-container.html", context)
    
    async def _generate_permutation(self) -> permutation:
        container: dependency_container = dependency_container.instance()
        i_dictionary: dictionary = container.get_dictionary().unwrap()
        i_cache: cache = container.get_cache().unwrap()
        i_permutation: permutation = await i_dictionary.generate_permutation()
        await i_cache.put(i_permutation.key(), i_permutation.struct())
        return i_permutation
    
    async def _find_result(self, body: Any):
        container: dependency_container = dependency_container.instance()
        reference = body["reference"]
        i_cache: cache = container.get_cache().unwrap()
        cached: optional[Any] = await i_cache.get(reference)
        if cached.is_some():
            return permutation(cached.unwrap()["base"], cached.unwrap()["result"])
        target = body["target"]
        i_dictionary: dictionary = container.get_dictionary().unwrap()
        i_permutation: permutation = await i_dictionary.generate_target_permutation(target)
        return i_permutation