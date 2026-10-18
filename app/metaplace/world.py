
from collections.abc import Iterator
from dataclasses import dataclass, field

from .places import PlacePresentation

Identifier = int | str

@dataclass(frozen=True, slots=True)
class Position:
    x: float = 0
    y: float = 0
    z: float = 0

@dataclass(slots=True)
class GameObject:
    """Represents an object positioned in a metaplace world."""

    object_id: int
    name: str = ''
    art_id: str = ''
    template_id: str = ''
    position: Position = field(default_factory=Position)
    facing: float = 0
    blocking: bool = False
    properties: dict[str, str] = field(default_factory=dict)

    @property
    def id(self) -> int:
        return self.object_id

    def move(self, x: float, y: float, z: float = 0) -> None:
        self.position = Position(x, y, z)

    def set_property(self, name: str, value: str) -> None:
        self.properties[name] = value

@dataclass(slots=True)
class PlaceInstance:
    """Represents a live instance of a place definition."""

    place: "Place"
    object_id: int = 0
    instance_id: str = '0'

    _objects: dict[int, GameObject] = field(
        default_factory=dict,
        init=False,
        repr=False
    )

    @property
    def objects(self) -> tuple[GameObject, ...]:
        return tuple(self._objects.values())

    def add_object(self, game_object: GameObject) -> GameObject:
        if game_object.object_id in self._objects:
            raise ValueError(f'Object {game_object.object_id} already exists')

        return self.upsert_object(game_object)

    def upsert_object(self, game_object: GameObject) -> GameObject:
        self._objects[game_object.object_id] = game_object
        return game_object

    def get_object(self, object_id: int) -> GameObject | None:
        return self._objects.get(object_id)

    def remove_object(self, object_id: int) -> GameObject:
        try:
            return self._objects.pop(object_id)
        except KeyError:
            raise KeyError(f'Object {object_id} does not exist') from None

@dataclass(slots=True)
class Place:
    """A reusable place definition for a metaplace world."""

    place_id: str
    name: str
    description: str = ''
    width: int = 0
    height: int = 0
    package_name: str = ''
    load_type: bool = False
    read_mode: bool = False
    persistent: bool = True
    presentation: PlacePresentation = field(default_factory=PlacePresentation)

    _instances: dict[str, PlaceInstance] = field(
        default_factory=dict,
        init=False,
        repr=False
    )

    @property
    def id(self) -> str:
        return self.place_id

    @property
    def instances(self) -> tuple[PlaceInstance, ...]:
        return tuple(self._instances.values())

    def instance(
        self,
        instance_id: str = '0',
        *,
        object_id: int | None = None,
    ) -> PlaceInstance:
        if (instance := self._instances.get(instance_id)) is not None:
            if object_id is not None and instance.object_id != object_id:
                raise ValueError(
                    f'Place instance {self.place_id}/{instance_id} already uses object {instance.object_id}'
                )
            return instance

        instance = PlaceInstance(
            self,
            object_id=object_id if object_id is not None else 0,
            instance_id=instance_id,
        )
        self._instances[instance_id] = instance
        return instance

    def remove_instance(self, instance_id: str) -> PlaceInstance:
        try:
            return self._instances.pop(instance_id)
        except KeyError:
            raise KeyError(f'Place instance {self.place_id}/{instance_id} does not exist') from None

@dataclass(slots=True)
class World:
    world_id: Identifier
    name: str
    owner: str = ''
    stylesheet_id: str = ''
    start_place_id: str | None = None
    clean_name: str = ''
    development_mode: str = '0'
    server_type: int = 0
    build_type: int = 1

    _places: dict[str, Place] = field(
        default_factory=dict,
        init=False,
        repr=False
    )
    _entry_place: PlaceInstance | None = field(
        default=None,
        init=False,
        repr=False,
    )

    @property
    def id(self) -> Identifier:
        return self.world_id

    @property
    def places(self) -> tuple[Place, ...]:
        return tuple(self._places.values())

    @property
    def entry_place(self) -> PlaceInstance | None:
        return self._entry_place

    def add_place(self, place: Place) -> Place:
        if place.place_id in self._places:
            raise ValueError(f'Place {place.place_id} already exists')

        self._places[place.place_id] = place
        return place

    def set_entry_place(
        self,
        place_id: str,
        *,
        object_id: int = 0,
        instance_id: str = '0',
    ) -> PlaceInstance:
        self._entry_place = self.require_place(place_id).instance(
            instance_id,
            object_id=object_id,
        )
        return self._entry_place

    def get_place(self, place_id: str) -> Place | None:
        return self._places.get(place_id)

    def require_place(self, place_id: str) -> Place:
        place = self.get_place(place_id)
        if place is None:
            raise KeyError(f'Place {place_id} does not exist in world {self.name}')
        return place

    def get_place_named(self, name: str) -> Place | None:
        return next((place for place in self._places.values() if place.name == name), None)

    def iter_instances(self) -> Iterator[PlaceInstance]:
        for place in self._places.values():
            yield from place.instances

class WorldCatalog:
    """Represents a catalog of metaplace worlds and their place mappings."""

    def __init__(self) -> None:
        self._worlds: dict[str, World] = {}
        self._place_routes: dict[tuple[str, str], tuple[str, str]] = {}

    @property
    def worlds(self) -> tuple[World, ...]:
        return tuple(self._worlds.values())

    def add_world(self, world: World) -> World:
        if world.name in self._worlds:
            raise ValueError(f'World {world.name!r} already exists')

        self._worlds[world.name] = world
        return world

    def get_world(self, name: str) -> World | None:
        return self._worlds.get(name)

    def map_place(
        self,
        product_name: str,
        place_name: str,
        world: World,
        place: Place,
    ) -> None:
        if self.get_world(world.name) is not world:
            raise ValueError('World must be registered before mapping a place')

        if world.get_place(place.place_id) is not place:
            raise ValueError('Place must belong to the mapped world')

        self._place_routes[(product_name, place_name)] = (world.name, place.place_id)

    def resolve_place(self, product_name: str, place_name: str) -> tuple[World, Place] | None:
        route = self._place_routes.get((product_name, place_name))

        if route is None:
            return None

        world_name, place_id = route
        world = self.get_world(world_name)
        if world is None:
            return None

        place = world.get_place(place_id)
        if place is None:
            return None

        return world, place
