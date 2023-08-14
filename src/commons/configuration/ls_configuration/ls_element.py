class ls_element():
    
    _id: str
    _clazz: str
    _name: str
    _api: str
    
    def __init__(self, id: str, clazz: str, name: str, api: str) -> None:
        self._id = id
        self._clazz = clazz
        self._name = name
        self._api = api
        
    def id(self):
        return self._id
    
    def clazz(self):
        return self._clazz
    
    def name(self):
        return self._name
    
    def api(self):
        return self._api