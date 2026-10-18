
from dataclasses import dataclass
from typing import Protocol, Any
from enum import Enum

from .serialization import AllowedValues
from .world import GameObject, PlaceInstance, World

import json

ClientEventPayload = AllowedValues | dict[str, Any] | list[Any]

class TagEmitter(Protocol):
    def __call__(self, name: str, /, *arguments: AllowedValues) -> None: ...

class SessionState(Enum):
    CONNECTED = 1
    AUTHENTICATED = 2
    IN_WORLD = 3
    PLACE_READY = 4
    CLOSED = 5

@dataclass(slots=True)
class MetaplaceSession:
    """Connection state for one player in one world"""

    world: World
    emit: TagEmitter
    player_id: int | None = None
    state: SessionState = SessionState.CONNECTED
    place: PlaceInstance | None = None

    def authenticate(self, player_id: int) -> None:
        if self.state is not SessionState.CONNECTED:
            raise RuntimeError('Session has already left the connected state')

        self.player_id = player_id
        self.state = SessionState.AUTHENTICATED

    def enter_world(self) -> None:
        if self.state is not SessionState.AUTHENTICATED or self.player_id is None:
            raise RuntimeError('Session must be authenticated before entering a world')

        if self.world.start_place_id is None:
            raise RuntimeError(f'World {self.world.name} has no start place')

        self.emit(
            'S_LOGIN',
            self.player_id,
        )
        self.emit(
            'S_WORLDTYPE',
            self.world.server_type,
            self.world.build_type,
            0, # TODO
        )
        self.emit(
            'S_WORLD',
            self.world.world_id,
            self.world.name,
            self.world.start_place_id,
            self.world.development_mode,
            'none', # TODO
            0, # TODO
            self.world.owner,
            self.world.clean_name or self.world.name,
            0, # TODO
            self.world.stylesheet_id,
            0, # TODO
        )
        self.state = SessionState.IN_WORLD

    def enter_place(self, place: PlaceInstance) -> PlaceInstance:
        if self.state not in (SessionState.IN_WORLD, SessionState.PLACE_READY):
            raise RuntimeError('Session must be in the world before entering a place')

        if self.world.get_place(place.place.place_id) is not place.place:
            raise ValueError('Place instance does not belong to this world')

        self.place = place
        self.emit('W_PLACE', place.place.place_id, place.object_id, place.instance_id)
        self.state = SessionState.PLACE_READY
        return self.place

    def show_object(self, game_object: GameObject) -> None:
        if self.place is None:
            raise RuntimeError('Session has no active place')

        self.place.upsert_object(game_object)

        self.emit(
            'O_HERE',
            game_object.object_id,
            game_object.art_id,
            game_object.position.x,
            game_object.position.y,
            game_object.position.z,
            1, # TODO
            0, # TODO
            0, # TODO
            0, # TODO
            game_object.name,
            game_object.template_id,
            int(game_object.blocking),
            1, # TODO
            0, # TODO
        )

        if not game_object.facing:
            return

        self.emit(
            'O_YAW',
            game_object.object_id,
            game_object.facing
        )

    def move_object(self, object_id: int, x: float, y: float, z: float = 0) -> None:
        game_object = self.require_object(object_id)
        game_object.move(x, y, z)
        self.emit('O_MOVE', object_id, x, y, z)

    def path_object(
        self,
        object_id: int,
        x: float,
        y: float,
        z: float,
        duration: int,
        replace: bool = True,
    ) -> None:
        game_object = self.require_object(object_id)
        game_object.move(x, y, z)
        self.emit('O_PATH', object_id, x, y, z, duration, replace)

    def remove_object(self, object_id: int) -> GameObject:
        if self.place is None:
            raise RuntimeError('Session has no active place')

        game_object = self.place.remove_object(object_id)
        self.emit('O_GONE', object_id)
        return game_object

    def send_client_event(
        self,
        object_id: int,
        name: str,
        payload: ClientEventPayload | None = None,
    ) -> None:
        if payload is None:
            self.emit('O_CLIENTEVENT', object_id, name)
            return

        if isinstance(payload, (dict, list)):
            payload = json.dumps(payload, separators=(',', ':'))

        self.emit('O_CLIENTEVENT', object_id, name, payload)

    def close(self) -> None:
        self.state = SessionState.CLOSED
        self.place = None

    def require_object(self, object_id: int) -> GameObject:
        if self.place is None:
            raise RuntimeError('Session has no active place')

        game_object = self.place.get_object(object_id)

        if game_object is None:
            raise KeyError(f'Object {object_id} does not exist in the active place')

        return game_object
