
from collections.abc import Iterable, Iterator
from .world import GameObject

class ObjectCollection:
    """Compatibility registry for callers migrating from Snowflake."""

    def __init__(self, objects: Iterable[GameObject] = (), offset: int = 0) -> None:
        self._objects: dict[int, GameObject] = {}
        self._next_id = offset + 1
        self.update(objects)

    def __iter__(self) -> Iterator[GameObject]:
        return iter(tuple(self._objects.values()))

    def __len__(self) -> int:
        return len(self._objects)

    def add(self, game_object: GameObject) -> None:
        if game_object.object_id < 0:
            game_object.object_id = self.get_id()

        if game_object.object_id in self._objects:
            raise ValueError(f'Object {game_object.object_id} already exists')

        self._objects[game_object.object_id] = game_object
        self._next_id = max(self._next_id, game_object.object_id + 1)

    def update(self, objects: Iterable[GameObject]) -> None:
        for game_object in objects:
            self.add(game_object)

    def remove(self, game_object: GameObject) -> None:
        del self._objects[game_object.object_id]

    def by_id(self, object_id: int) -> GameObject | None:
        return self._objects.get(object_id)

    def by_name(self, name: str) -> GameObject | None:
        return next((game_object for game_object in self if game_object.name == name), None)

    def by_name_required(self, name: str) -> GameObject:
        game_object = self.by_name(name)

        if game_object is None:
            raise KeyError(f'Object named {name!r} does not exist')

        return game_object

    def get_id(self) -> int:
        return self._next_id
