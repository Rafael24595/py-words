import json
from commons.optional import optional

from domain.ascii import ascii
from domain.ascii_form import ascii_form
from domain.ascii_gray_scale import ascii_gray_scale
from domain.ascii_image import ascii_image
from domain.ascii_persistence import ascii_persistence

class ascii_memory(ascii):

    NAME: str = "ascii_memory"
    __count: int
    
    def __init__(self, *args: dict[str, str]) -> None:
        self.__count = 0

    def enablePersistence(self, persistence: ascii_persistence):
        pass

    async def get_gray_scales(self) -> list[ascii_gray_scale]:
        return [ascii_gray_scale("DEFAULT", "DEFAULT"), 
            ascii_gray_scale("SOUP_CAHOS_SOFT", "SOUP_CAHOS_SOFT"),
            ascii_gray_scale("SOUP_CAHOS_HARD", "SOUP_CAHOS_HARD")]

    async def generate_ascii(self, form: ascii_form) -> ascii_image:
        file = None
        if self.__count % 2 == 0:
            file = open('assets/app/go-ascii/configuration/mock-gif.json')
        else:
            file = open('assets/app/go-ascii/configuration/mock-png.json')
        self.__count = self.__count + 1
        dto = json.load(file)
        return ascii_image(dto["name"], dto["extension"], dto["height"], 
            dto["width"], dto["status"], dto["message"], 
            dto["frames"])
    
    async def take(self, key: str) -> optional[ascii_image]:
        return optional.some(await self.generate_ascii(""))
    
    async def takeAll(self) -> list[ascii_image]:
        images: list[ascii_image] = []
        for _ in range(2):
            images.append(await self.generate_ascii(""))
        return images