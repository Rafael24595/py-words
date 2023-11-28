from fastapi.templating import Jinja2Templates
from commons.configuration.configuration import configuration
from infrastructure.petition.i_py_petition import i_py_petition

BASE: str = "index"

class ui_builder_index():
    
    _templates = Jinja2Templates(directory="assets/index")
    
    @classmethod
    def build(cls, petition: i_py_petition):
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
        
        context = { 'request': petition.get_request(), 'base': BASE, 'headers': headers, 'body': body, 'footers': footers }
        template = cls._templates.TemplateResponse("index.html", context)
        
        petition.add_context(template)