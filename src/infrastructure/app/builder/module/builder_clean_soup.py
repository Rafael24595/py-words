from fastapi.templating import Jinja2Templates

from fastapi import Request

NAME: str = "clean-soup"

class builder_clean_soup():
    
    _templates = Jinja2Templates(directory="assets/app")
    
    @classmethod
    async def build(cls, request: Request):
        return "<h1>" + NAME + "</h1>"