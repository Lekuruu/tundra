
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

    def serialize(self) -> str:
        return "|".join(
            str(getattr(self, part))
            for part in self.model_fields.keys()
        )
