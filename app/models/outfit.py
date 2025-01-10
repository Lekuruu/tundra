
from __future__ import annotations
from pydantic import BaseModel

class Outfit(BaseModel):
    colour: int
    head: int
    face: int
    neck: int
    body: int
    hand: int
    feet: int
    flag: int
    photo: int
