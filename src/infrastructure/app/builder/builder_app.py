from fastapi.templating import Jinja2Templates

from fastapi import Request
from infrastructure.app.builder.module.builder_clean_soup import builder_clean_soup

from infrastructure.app.builder.module.builder_rust_dictionary import builder_rust_dictionary
from infrastructure.index.builder.builder_index import builder_index

class builder_app():
        
    @classmethod
    async def build(cls, code: str, request: Request) -> str:
        return await cls._build_module(code, request)
        
    @classmethod
    async def _build_module(cls, code: str, request: Request) -> str:
        match code:
            case "rust-dictionary":
                return await builder_rust_dictionary.build(request)
            case "clean-soup":
                return await builder_clean_soup.build(request)
            
        return builder_index.build(request)