from typing import Any
from fastapi.templating import Jinja2Templates

from fastapi import Request

from commons.configuration.dependency.dependency_container import dependency_container
from commons.optional import optional
from domain.cache import cache
from domain.clue import clue
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
            case "new-clue":
                return await self._build_new_clue(request)
            case "update-score":
                return await self._update_score(request)
    
    async def _build_result(self, request: Request):
        i_permutation: permutation = await self._find_result(request)
        return str(i_permutation.struct())
    
    async def _build_added_words(self, request: Request):
        body: map[str,Any] = await request.json()
        words: list[str] = await self._added_words(request)
        add_word_raw = body.get('add-word')
        if add_word_raw not in words and add_word_raw != None:
            words = [add_word_raw] + words
        context = { 'request': request, 'base': BASE, 'words':  words}
        return self._templates.TemplateResponse("added-word-container.html", context)
    
    async def _build_remove_words(self, request: Request):
        words: list[str] = await self._added_words(request)
        word = request.query_params.get("word")
        if word in words:
            words.remove(word)
        context = { 'request': request, 'base': BASE, 'words':  words}
        return self._templates.TemplateResponse("added-word-container.html", context)
    
    async def _added_words(self, request: Request) -> list[str]:
        body: map[str,Any] = await request.json()
        words = []
        added_words_raw = body.get('added-word')
        if isinstance(added_words_raw, list):
            words = added_words_raw
        elif not added_words_raw == None:
            words = [added_words_raw]
        return words
    
    async def _build_new_clue(self, request: Request):
        clues: list[str] = await self._added_clues(request)
        clue: list[str] = await self._find_clue(request, clues)
        clues = clues + clue
        context = { 'request': request, 'base': BASE, 'clues': clues}
        return self._templates.TemplateResponse("added-clues-container.html", context)
    
    async def _find_clue(self, request: Request, clues: list[str]) -> list[str]:
        i_permutation: permutation = await self._find_result(request)
        new_clues: list[clue] = i_permutation.find_different_clues(clues)
        if len(new_clues) > 0:
            return [new_clues[0].clue()]
        return []
    
    async def _update_score(self, request: Request):
        clues: list[str] = await self._added_clues(request)
        score: int = 0
        i_permutation: permutation = await self._find_result(request)
        for cl in i_permutation.find_clues(clues):
            score = score - cl.score()
        return str(score)
    
    async def _added_clues(self, request: Request):
        body: map[str,Any] = await request.json()
        added_clues_raw = body.get('added-clue')
        clues: list[str] = []
        if isinstance(added_clues_raw, list):
            clues = added_clues_raw
        elif not added_clues_raw == None:
            clues = [added_clues_raw]
        return clues
    
    async def _generate_permutation(self) -> permutation:
        container: dependency_container = dependency_container.instance()
        i_dictionary: dictionary = container.get_dictionary().unwrap()
        i_cache: cache = container.get_cache().unwrap()
        i_permutation: permutation = await i_dictionary.generate_permutation()
        await i_cache.put(i_permutation.key(), i_permutation.struct())
        return i_permutation
    
    async def _find_result(self, request: Request) -> permutation:
        body: Any = await request.json()
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