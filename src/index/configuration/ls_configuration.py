import json
from commons.Optional import Optional
from .ls_element import ls_element

class ls_configuration():
    
    instance: 'Optional[ls_configuration]' = Optional.none()
    
    _elements: list[ls_element] = []
    
    @classmethod
    def get_instance(cls) -> 'ls_configuration':
        if cls.instance.is_none():
            cls.instance = Optional.some(cls.load())
        return cls.instance.unwrap()
    
    @classmethod
    def load(cls) -> 'ls_configuration':
        config: ls_configuration = ls_configuration()
        f = open('src/index/configuration/configuration.json')
        elements = json.load(f)
        for element in elements:
            lse: ls_element = ls_element(element["id"], element["clazz"], element["path"], element["template"])
            config._elements.append(lse)
        f.close()
        return config
    
    def json_elements(self) -> list[dict[str, str]]:
        vector: list[dict[str, str]] = []
        for element in self._elements:
            struct: dict[str, str] = {
                "id": element.id(),
                "class": element.clazz(),
                "path": element.path(),
                "template": element.template()
            }
            
            vector.append(struct)
        return vector