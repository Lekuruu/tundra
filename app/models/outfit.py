
from pydantic import BaseModel, field_serializer, field_validator

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

    @field_validator("*")
    @classmethod
    def normalize_empty_slot(cls, item_id: int) -> int:
        if item_id < -1:
            raise ValueError("Outfit item IDs must be -1 or greater")

        # The mobile client uses both 0 & -1 to represent an empty slot
        return -1 if item_id == 0 else item_id

    @classmethod
    def deserialize(cls, value: str) -> "Outfit":
        parts = value.split("|")

        if len(parts) != len(cls.model_fields):
            raise ValueError("An outfit must contain exactly nine item slots")

        try:
            item_ids = [int(part) for part in parts]
        except ValueError as exc:
            raise ValueError("Outfit slots must be integer item IDs") from exc

        return cls(**dict(zip(cls.model_fields, item_ids)))

    def serialize(self) -> str:
        return "|".join(
            str(getattr(self, part))
            for part in type(self).model_fields
        )

class OutfitPayload(BaseModel):
    # Client example: {"outfit": "15|-1|-1|-1|-1|-1|6163|-1|-1"}
    outfit: Outfit

    @field_validator("outfit", mode="before", json_schema_input_type=str)
    @classmethod
    def deserialize_outfit(cls, value: object) -> Outfit:
        if isinstance(value, Outfit):
            return value

        if not isinstance(value, str):
            raise ValueError("An outfit must be a pipe-delimited string")

        return Outfit.deserialize(value)

    @field_serializer("outfit", return_type=str)
    def serialize_outfit(self, outfit: Outfit) -> str:
        return outfit.serialize()
