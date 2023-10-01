from typing import Any
from fastapi.templating import Jinja2Templates

from commons.configuration.dependency.dependency_container import dependency_container
from commons.optional import optional
from domain.cache import cache
from domain.cache_event import cache_event
from domain.clue import clue
from domain.dictionary import dictionary
from domain.permutation import permutation
from domain.permutation_result import permutation_result
from infrastructure.app.builder.module.rust_dictionary_actions import rust_dictionary_actions
from infrastructure.app.builder.module.ui_builder_module_app import ui_builder_module_app
from infrastructure.petition.i_py_petition import i_py_petition

class ui_builder_rust_dictionary(ui_builder_module_app):
    
    _templates = Jinja2Templates
    
    def __init__(self) -> None:
        self._templates = Jinja2Templates(directory="assets/app/" + rust_dictionary_actions.APP.value)

    async def build(self, petition: i_py_petition):
        i_permutation: permutation = await self._generate_permutation()
        j_permutation = {
            'target': i_permutation.get_base(),
            'reference': i_permutation.key()
        }
        context = { 
            'request': petition.get_request(), 
            'app': rust_dictionary_actions.APP.value, 
            'action_add_word': rust_dictionary_actions.ADD_WORD.value, 
            'action_resolve': rust_dictionary_actions.RESOLVE.value, 
            'action_new_clue': rust_dictionary_actions.NEW_CLUE.value, 
            'action_update_score': rust_dictionary_actions.UPDATE_SCORE.value, 
            'permutation': j_permutation 
        }
        template = self._templates.TemplateResponse("index.html", context)
        petition.add_context(template)

    async def execute(self, action: str, petition: i_py_petition):
        match(action):
            case rust_dictionary_actions.RESOLVE.value:
                if not await self._is_finished(petition):
                    return await self._build_result(petition)
                return self._cancel_request(petition)
            case rust_dictionary_actions.ADD_WORD.value:
                if not await self._is_finished(petition):
                    return await self._build_added_words(petition)
                return self._cancel_request(petition)
            case rust_dictionary_actions.REMOVE_WORD.value:
                if not await self._is_finished(petition):
                    return await self._build_remove_words(petition)
                return self._cancel_request(petition)
            case rust_dictionary_actions.NEW_CLUE.value:
                if not await self._is_finished(petition):
                    return await self._build_new_clue(petition)
                return self._cancel_request(petition)
            case rust_dictionary_actions.UPDATE_SCORE.value:
                if not await self._is_finished(petition):
                    return await self._build_score(petition, False)
                return self._cancel_request(petition)
            case rust_dictionary_actions.RESOLVE_SCORE.value:
                return await self._build_score(petition, True)
        return None
    
    async def _build_result(self, petition: i_py_petition):
        i_permutation: permutation = await self._find_result(petition)
        result: permutation_result = await self._permutation_result(petition)
        clues: list[str] = await self._added_clues(petition)
        messages: list[str] = []
        messages.append("Found words " + str(len(result.found())) + " of " + str(len(i_permutation.get_result())) + ": " + str(result.found()))
        messages.append("Forgotten words " + str(len(result.forgotten())) + " of " + str(len(i_permutation.get_result())) + ": " + str(result.forgotten()))
        messages.append("Mistaked words " + str(len(result.mistaked())) + ": " + str(result.mistaked()))
        messages.append("Clues used: " + str(len(clues)))
        context = { 
            'request': petition.get_request(), 
            'app': rust_dictionary_actions.APP.value, 
            'action_resolve_score': rust_dictionary_actions.RESOLVE_SCORE.value, 
            'messages':  messages
        }
        template =  self._templates.TemplateResponse("added-result-container.html", context)
        petition.add_context(template)
    
    async def _build_added_words(self, petition: i_py_petition):
        body: dict[str,Any] = await petition.input_json()
        words: list[str] = await self._added_words(petition)
        add_word_raw = body.get('add-word')
        if add_word_raw not in words and add_word_raw != None:
            words = [add_word_raw] + words
        return self._build_words(petition, words)
    
    async def _build_remove_words(self, petition: i_py_petition):
        words: list[str] = await self._added_words(petition)
        word = petition.input_param_query("word").unwrap()
        if word in words:
            words.remove(word)
        return self._build_words(petition, words)
    
    def _build_words(self, petition: i_py_petition, words: list[str]):
        context = { 
            'request': petition.get_request(), 
            'app': rust_dictionary_actions.APP.value, 
            'action_remove_word': rust_dictionary_actions.REMOVE_WORD.value, 
            'words':  words
        }
        template =  self._templates.TemplateResponse("added-word-container.html", context)
        petition.add_context(template)
    
    async def _build_new_clue(self, petition: i_py_petition):
        clues: list[str] = await self._added_clues(petition)
        clue: list[str] = await self._find_clue(petition, clues)
        clues = clues + clue
        context = { 
            'request': petition.get_request(),
            'clues': clues
        }
        template = self._templates.TemplateResponse("added-clues-container.html", context)
        petition.add_context(template)
    
    async def _build_score(self, petition: i_py_petition, resolve: bool):
        score: int = await self._calculate_score(petition, resolve)
        status: str = ""
        if score < 0:
            status = "failed"
        if score > 0:
            status = "successed"
        context = { 
            'request': petition.get_request(), 
            'score': str(score), 
            'status': status
        }
        template = self._templates.TemplateResponse("score-container.html", context)
        petition.add_context(template)
    
    async def _calculate_score(self, petition: i_py_petition, resolve: bool) -> int:
        clues: list[str] = await self._added_clues(petition)
        score: int = 0
        i_permutation: permutation = await self._find_result(petition)
        for cl in i_permutation.find_clues(clues):
            score = score - cl.score()
        if resolve:
            result: permutation_result = await self._permutation_result(petition)
            score = score + len(result.found()) * 50
            score = score + len(result.mistaked()) * 100 * -1
        return score
    
    async def _generate_permutation(self) -> permutation:
        container: dependency_container = dependency_container.instance()
        i_dictionary: dictionary = container.get_dictionary().unwrap()
        i_cache: cache = container.get_cache().unwrap()
        i_permutation: permutation = await i_dictionary.generate_permutation()
        await i_cache.put(i_permutation.key(), "global", i_permutation.struct())
        return i_permutation
    
    async def _permutation_result(self, petition: i_py_petition) -> permutation_result:
        i_permutation: permutation = await self._find_result(petition)
        words: list[str] = await self._added_words(petition)
        return i_permutation.evalue_result(words)
    
    async def _find_result(self, petition: i_py_petition) -> permutation:
        body: dict[str,Any] = await petition.input_json()
        container: dependency_container = dependency_container.instance()
        reference = body.get("reference")
        i_cache: cache = container.get_cache().unwrap()
        event: optional[cache_event[dict[str,str]]] = await i_cache.get(reference)
        if event.is_some():
            struct = event.unwrap().data()
            return permutation(struct["base"], struct["result"])
        target = body.get("target")
        i_dictionary: dictionary = container.get_dictionary().unwrap()
        i_permutation: permutation = await i_dictionary.generate_target_permutation(target)
        return i_permutation
    
    async def _added_words(self, petition: i_py_petition) -> list[str]:
        body: dict[str,Any] = await petition.input_json()
        words = []
        added_words_raw = body.get('added-word')
        if isinstance(added_words_raw, list):
            words = added_words_raw
        elif not added_words_raw == None:
            words = [added_words_raw]
        return words
    
    async def _added_clues(self, petition: i_py_petition):
        body: dict[str,Any] = await petition.input_json()
        added_clues_raw = body.get('added-clue')
        clues: list[str] = []
        if isinstance(added_clues_raw, list):
            clues = added_clues_raw
        elif not added_clues_raw == None:
            clues = [added_clues_raw]
        return clues
    
    async def _find_clue(self, petition: i_py_petition, clues: list[str]) -> list[str]:
        i_permutation: permutation = await self._find_result(petition)
        new_clues: list[clue] = i_permutation.find_different_clues(clues)
        if len(new_clues) > 0:
            return [new_clues[0].clue()]
        return []
    
    async def _is_finished(self, petition: i_py_petition) -> bool:
        body: dict[str,Any] = await petition.input_json()
        finished = body.get("finished")
        return finished is not None and finished
    
    def _cancel_request(self, petition: i_py_petition) -> None:
        petition.add_header("HX-Retarget", "#void-container")
        return None