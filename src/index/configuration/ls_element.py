class ls_element():
    
    _id: str
    _clazz: str
    _path: str
    _template: str
    
    def __init__(self, id: str, clazz: str, path: str, template: str) -> None:
        self._id = id
        self._clazz = clazz
        self._path = path
        self._template = template
        
    def id(self):
        return self._id
    
    def clazz(self):
        return self._clazz
    
    def path(self):
        return self._path
    
    def template(self):
        return self._template