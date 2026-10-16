
from pydantic import BaseModel


class Items(BaseModel):
    COLOUR: list[int]
    HEAD: list[int]
    FACE: list[int]
    NECK: list[int]
    BODY: list[int]
    HAND: list[int]
    FEET: list[int]
    FLAG: list[int]
    PHOTO: list[int]
    OTHER: list[int]
