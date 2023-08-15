from fastapi.templating import Jinja2Templates

from fastapi import Request
from commons.optional import optional

from commons.configuration.dependency.dependency_container import dependency_container
from domain.dictionary import dictionary

NAME: str = "rust-dictionary"

class builder_rust_dictionary():
    
    _templates = Jinja2Templates(directory="assets/app")
    
    @classmethod
    async def build(cls, request: Request):
        d: optional[dictionary] = dependency_container.instance().get_dictionary()
        perm = await d.unwrap().generate_permutation()
        return "<h1>" + NAME + "</h1><br><p>" + perm.get_base() + "</p>"