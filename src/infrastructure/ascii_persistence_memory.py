from commons.optional import optional

from domain.ascii_image import ascii_image
from domain.ascii_persistence import ascii_persistence

class ascii_persistence_memory(ascii_persistence):

    NAME: str = "ascii_persistence_memory"
    
    __persistence: dict[str, ascii_image]
    
    def __init__(self, args: dict[str, str]) -> None:
        self.__persistence = {}

    async def put(self, image: ascii_image) -> ascii_image:
        self.__persistence[image.name()] = image
    
    async def take(self, key: str) -> optional[ascii_image]:
        image = self.__persistence.get(key)
        if image is None:
            return optional.none()
        return optional.some(image)
    
    async def takeAll(self) -> list[ascii_image]:
        items = []
        for _, value in self.__persistence.items():
            items.append(value)
        return items