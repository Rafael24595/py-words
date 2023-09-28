from fastapi.templating import Jinja2Templates

from fastapi import Request, Response
from commons.configuration.configuration import configuration

BASE: str = "index"

class ui_builder_index():
    
    _templates = Jinja2Templates(directory="assets/index")
    
    @classmethod
    def build(cls, request: Request, response: Response):
        conf: configuration = configuration.instance()
        headers = []
        footers = []
        ls_conf = conf.left_sidebar
        body = {
            'ls_sidebar': {
                "title": ls_conf.title(),
                "elements": ls_conf.json_elements()
            }
        }
        context = { 'request': request, 'base': BASE, 'headers': headers, 'body': body, 'footers': footers }
        return cls._templates.TemplateResponse("index.html", context)