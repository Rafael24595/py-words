from typing import Any
from fastapi.templating import Jinja2Templates

from fastapi import Request, Response

from commons.configuration.dependency.dependency_container import dependency_container
from commons.optional import optional
from domain.cache import cache
from domain.clue import clue
from domain.dictionary import dictionary
from domain.permutation import permutation
from domain.permutation_result import permutation_result
from infrastructure.app.builder.module.rust_dictionary_actions import rust_dictionary_actions
from infrastructure.app.builder.module.ui_builder_module_app import ui_builder_module_app

class ui_builder_rust_dictionary(ui_builder_module_app):
    
    _templates = Jinja2Templates
    
    def __init__(self) -> None:
        self._templates = Jinja2Templates(directory="assets/app/" + rust_dictionary_actions.APP.value)

    async def build(self, request: Request, response: Response):
        i_permutation: permutation = await self._generate_permutation()
        j_permutation = {
            'target': i_permutation.get_base(),
            'reference': i_permutation.key()
        }
        context = { 
            'request': request, 
            'app': rust_dictionary_actions.APP.value, 
            'action_add_word': rust_dictionary_actions.ADD_WORD.value, 
            'action_resolve': rust_dictionary_actions.RESOLVE.value, 
            'action_new_clue': rust_dictionary_actions.NEW_CLUE.value, 
            'action_update_score': rust_dictionary_actions.UPDATE_SCORE.value, 
            'permutation': j_permutation 
        }
        return self._templates.TemplateResponse("index.html", context)

    async def execute(self, action: str, request: Request, response: Response):
        match(action):
            case rust_dictionary_actions.RESOLVE.value:
                if not await self._is_finished(request):
                    return await self._build_result(request)
                return self._cancel_request(response)
            case rust_dictionary_actions.ADD_WORD.value:
                if not await self._is_finished(request):
                    return await self._build_added_words(request)
                return self._cancel_request(response)
            case rust_dictionary_actions.REMOVE_WORD.value:
                if not await self._is_finished(request):
                    return await self._build_remove_words(request)
                return self._cancel_request(response)
            case rust_dictionary_actions.NEW_CLUE.value:
                if not await self._is_finished(request):
                    return await self._build_new_clue(request)
                return self._cancel_request(response)
            case rust_dictionary_actions.UPDATE_SCORE.value:
                if not await self._is_finished(request):
                    return await self._build_score(request, False)
                return self._cancel_request(response)
            case rust_dictionary_actions.RESOLVE_SCORE.value:
                return await self._build_score(request, True)
        return None
    
    async def _build_result(self, request: Request):
        i_permutation: permutation = await self._find_result(request)
        result: permutation_result = await self._permutation_result(request)
        clues: list[str] = await self._added_clues(request)
        messages: list[str] = []
        messages.append("Found words " + str(len(result.found())) + " of " + str(len(i_permutation.get_result())) + ": " + str(result.found()))
        messages.append("Forgotten words " + str(len(result.forgotten())) + " of " + str(len(i_permutation.get_result())) + ": " + str(result.forgotten()))
        messages.append("Mistaked words " + str(len(result.mistaked())) + ": " + str(result.mistaked()))
        messages.append("Clues used: " + str(len(clues)))
        context = { 
            'request': request, 
            'app': rust_dictionary_actions.APP.value, 
            'action_resolve_score': rust_dictionary_actions.RESOLVE_SCORE.value, 
            'messages':  messages
        }
        return self._templates.TemplateResponse("added-result-container.html", context)
    
    async def _build_added_words(self, request: Request):
        body: dict[str,Any] = await request.json()
        words: list[str] = await self._added_words(request)
        add_word_raw = body.get('add-word')
        if add_word_raw not in words and add_word_raw != None:
            words = [add_word_raw] + words
        return self._build_words(request, words)
    
    async def _build_remove_words(self, request: Request):
        words: list[str] = await self._added_words(request)
        word = request.query_params.get("word")
        if word in words:
            words.remove(word)
        return self._build_words(request, words)
    
    def _build_words(self, request: Request, words: list[str]):
        context = { 
            'request': request, 
            'app': rust_dictionary_actions.APP.value, 
            'action_remove_word': rust_dictionary_actions.REMOVE_WORD.value, 
            'words':  words
        }
        return self._templates.TemplateResponse("added-word-container.html", context)
    
    async def _build_new_clue(self, request: Request):
        clues: list[str] = await self._added_clues(request)
        clue: list[str] = await self._find_clue(request, clues)
        clues = clues + clue
        context = { 
            'request': request,
            'clues': clues
        }
        return self._templates.TemplateResponse("added-clues-container.html", context)
    
    async def _build_score(self, request: Request, resolve: bool):
        score: int = await self._calculate_score(request, resolve)
        status: str = ""
        if score < 0:
            status = "failed"
        if score > 0:
            status = "successed"
        context = { 
            'request': request, 
            'score': str(score), 
            'status': status
        }
        return self._templates.TemplateResponse("score-container.html", context)
    
    async def _calculate_score(self, request: Request, resolve: bool) -> int:
        clues: list[str] = await self._added_clues(request)
        score: int = 0
        i_permutation: permutation = await self._find_result(request)
        for cl in i_permutation.find_clues(clues):
            score = score - cl.score()
        if resolve:
            result: permutation_result = await self._permutation_result(request)
            score = score + len(result.found()) * 50
            score = score + len(result.mistaked()) * 100 * -1
        return score
    
    async def _generate_permutation(self) -> permutation:
        container: dependency_container = dependency_container.instance()
        i_dictionary: dictionary = container.get_dictionary().unwrap()
        i_cache: cache = container.get_cache().unwrap()
        i_permutation: permutation = await i_dictionary.generate_permutation()
        await i_cache.put(i_permutation.key(), i_permutation.struct())
        return i_permutation
    
    async def _permutation_result(self, request: Request) -> permutation_result:
        i_permutation: permutation = await self._find_result(request)
        words: list[str] = await self._added_words(request)
        return i_permutation.evalue_result(words)
    
    async def _find_result(self, request: Request) -> permutation:
        body: dict[str,Any] = await request.json()
        container: dependency_container = dependency_container.instance()
        reference = body.get("reference")
        i_cache: cache = container.get_cache().unwrap()
        cached: optional[Any] = await i_cache.get(reference)
        if cached.is_some():
            return permutation(cached.unwrap()["base"], cached.unwrap()["result"])
        target = body.get("target")
        i_dictionary: dictionary = container.get_dictionary().unwrap()
        i_permutation: permutation = await i_dictionary.generate_target_permutation(target)
        return i_permutation
    
    async def _added_words(self, request: Request) -> list[str]:
        body: dict[str,Any] = await request.json()
        words = []
        added_words_raw = body.get('added-word')
        if isinstance(added_words_raw, list):
            words = added_words_raw
        elif not added_words_raw == None:
            words = [added_words_raw]
        return words
    
    async def _added_clues(self, request: Request):
        body: dict[str,Any] = await request.json()
        added_clues_raw = body.get('added-clue')
        clues: list[str] = []
        if isinstance(added_clues_raw, list):
            clues = added_clues_raw
        elif not added_clues_raw == None:
            clues = [added_clues_raw]
        return clues
    
    async def _find_clue(self, request: Request, clues: list[str]) -> list[str]:
        i_permutation: permutation = await self._find_result(request)
        new_clues: list[clue] = i_permutation.find_different_clues(clues)
        if len(new_clues) > 0:
            return [new_clues[0].clue()]
        return []
    
    async def _is_finished(self, request: Request) -> bool:
        body: dict[str,Any] = await request.json()
        finished = body.get("finished")
        return finished is not None and finished
    
    def _cancel_request(self, response: Response) -> None:
        response.headers["HX-Retarget"] = "#void-container"
        return None