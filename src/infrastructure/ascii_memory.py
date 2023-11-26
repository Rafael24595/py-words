import json

from domain.ascii import ascii
from domain.ascii_form import ascii_form
from domain.ascii_image import ascii_image

class ascii_memory(ascii):

    NAME: str = "ascii_memory"
    
    def __init__(self, *args: dict[str, str]) -> None:
        pass

    async def generate_ascii(self, form: ascii_form) -> ascii_image:
        file = open('assets/app/go-ascii/configuration/mock-gif.json')
        dto = json.load(file)
        return ascii_image(dto["name"], dto["extension"], dto["height"], 
            dto["width"], dto["status"], dto["message"], 
            dto["frames"])
    
    async def take(self, key: str) -> ascii_image:
        return self.generate_ascii("")
    
    async def takeAll(self) -> list[ascii_image]:
        return [self.generate_ascii("")]