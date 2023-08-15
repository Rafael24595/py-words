import json
from commons.optional import optional
from .ls_element import ls_element

class ls_configuration():
    
    singleton: 'optional[ls_configuration]' = optional.none()
    
    _title: str = ""
    _elements: list[ls_element] = []
    
    @classmethod
    def instance(cls) -> 'ls_configuration':
        if cls.singleton.is_none():
            cls.singleton = optional.some(cls.load())
        return cls.singleton.unwrap()
    
    @classmethod
    def load(cls) -> 'ls_configuration':
        config: ls_configuration = ls_configuration()
        f = open('src/commons/configuration/ls_configuration/ls_configuration.json')
        data = json.load(f)
        config._title = data["title"]
        for element in data["elements"]:
            lse: ls_element = ls_element(element["id"], element["clazz"], element["name"], element["api"])
            config._elements.append(lse)
        f.close()
    
        return config
    
    def title(self) -> str:
        return self._title
    
    def json_elements(self) -> list[dict[str, str]]:
        vector: list[dict[str, str]] = []
        for element in self._elements:
            struct: dict[str, str] = {
                "id": element.id(),
                "clazz": element.clazz(),
                "name": element.name(),
                "api": element.api()
            }
            
            vector.append(struct)
        return vector