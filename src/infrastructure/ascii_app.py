import time
from typing import Any

import requests
from commons.optional import optional

from domain.ascii import ascii
from domain.ascii_form import ascii_form
from domain.ascii_gray_scale import ascii_gray_scale
from domain.ascii_image import ascii_image
from domain.ascii_persistence import ascii_persistence

class ascii_app(ascii):

    NAME: str = "ascii_app"
    
    __connection: str
    __ascii_persistence: optional[ascii_persistence]
    
    def __init__(self, args: dict[str, str]) -> None:
        self.__connection = args["SERVICE_ASCII_CONNECTION"]
        self.__ascii_persistence = optional.none()

    def enablePersistence(self, persistence: ascii_persistence):
        self.__ascii_persistence = optional.some(persistence)

    async def get_gray_scales(self) -> list[ascii_gray_scale]:
        response = requests.get(self.__connection + "api/gray_scale")
        json: list[dict[str,Any]] = response.json()
        scales = []
        for scale in json:
            scales.append(ascii_gray_scale(scale["id"], scale["description"]))
        return scales

    async def generate_ascii(self, form: ascii_form) -> ascii_image:
        response = requests.post(self.__connection + "api/ascii", json=form.to_dict())
        id: str = response.json()
        ##TODO: Fix endless loop.
        creating = True
        while creating:
            image = await self.__take_service(id)
            if image.is_some():
                await self.__put(image.unwrap())
                return image.unwrap()
            time.sleep(1)
        return None
    
    async def __take_service(self, key: str) -> optional[ascii_image]:
        response = requests.get(self.__connection + "api/ascii/" + key)
        if response.status_code == 404:
            return optional.none()
        json: dict[str,Any] = response.json()
        return optional.some(ascii_image(json["name"], json["extension"], json["height"], 
            json["width"], json["status"], json["message"], 
            json["frames"]))
    
    async def take(self, key: str) -> optional[ascii_image]:
        if self.__ascii_persistence.is_none():
            #TODO: Log
            return optional.none()
        return await self.__ascii_persistence.unwrap().take(key)
    
    async def takeAll(self) -> list[ascii_image]:
        if self.__ascii_persistence.is_none():
            #TODO: Log
            return []
        return await self.__ascii_persistence.unwrap().takeAll()
    
    async def __put(self, image: ascii_image) -> optional[ascii_image]:
        if self.__ascii_persistence.is_some():
            return optional.some(await self.__ascii_persistence.unwrap().put(image))
        return optional.none()