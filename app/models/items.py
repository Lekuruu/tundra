
from __future__ import annotations
from pydantic import BaseModel
from typing import List

class Items(BaseModel):
    colour: List[int]
    head: List[int]
    face: List[int]
    neck: List[int]
    body: List[int]
    hand: List[int]
    feet: List[int]
    flag: List[int]
    photo: List[int]
    award: List[int]
