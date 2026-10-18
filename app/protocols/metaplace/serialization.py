
import json
from dataclasses import dataclass
from typing import Any

# beware of the hacky mess that is following here
# i really hate the way of decoding / encoding this

AllowedValues = str | int | float | bool | None

def encode_value(value: AllowedValues) -> str:
    if value is None:
        return ''
    if isinstance(value, bool):
        return str(int(value))
    return str(value)

@dataclass(frozen=True, slots=True)
class Tag:
    name: str
    arguments: tuple[AllowedValues, ...] = ()

    def encode(self) -> bytes:
        # e.g. Tag('S_WORLDTYPE', (0, 1, 0)) becomes b'[S_WORLDTYPE]|0|1|0|\r\n'
        values = '|'.join(encode_value(value) for value in self.arguments)
        suffix = f'|{values}|' if self.arguments else '|'
        return f'[{self.name}]{suffix}\r\n'.encode()

    @classmethod
    def decode(cls, data: bytes | str) -> "Tag":
        text = data.decode('utf-8') if isinstance(data, bytes) else data
        text = text.strip()

        if not text.startswith('[') or ']' not in text:
            raise ValueError('Invalid metaplace tag')

        closing = text.index(']')
        name = text[1:closing]
        payload = text[closing + 1:]

        if payload == '|':
            arguments = ()
        elif payload.startswith('|') and payload.endswith('|'):
            arguments = tuple(payload[1:-1].split('|'))
        else:
            raise ValueError('Invalid metaplace tag payload')

        return cls(name, arguments)

@dataclass(frozen=True, slots=True)
class Command:
    name: str
    arguments: tuple[str | dict[str, Any] | list[Any], ...] = ()

    @classmethod
    def decode(cls, data: bytes | str) -> "Command":
        text = data.decode('utf-8') if isinstance(data, bytes) else data
        text = text.strip()

        if not text:
            raise ValueError('Empty metaplace command')

        name, separator, payload = text.partition(' ')
        if not separator:
            return cls(name)

        payload = payload.strip()
        if payload.startswith(('{', '[')):
            # yeah, kinda hacky but w/e
            try:
                value = json.loads(payload)
            except json.JSONDecodeError:
                pass
            else:
                return cls(name, (value,))

        return cls(name, tuple(payload.split()))
