
from collections.abc import Callable, Iterable, Mapping
from typing import TYPE_CHECKING
import logging

from .serialization import Command

if TYPE_CHECKING:
    from .protocol import MetaplaceProtocol
    from .world import GameObject

CommandHandler = Callable[['MetaplaceProtocol', Command], None]

class MetaplacePlugin:
    """Adds application behavior to a metaplace protocol factory."""

    def command_handlers(self) -> Mapping[str, CommandHandler]:
        return {}

    def on_connected(self, protocol: 'MetaplaceProtocol') -> None:
        pass

    def on_disconnected(self, protocol: 'MetaplaceProtocol') -> None:
        pass

    def on_player_ready(self, protocol: 'MetaplaceProtocol', player: 'GameObject') -> None:
        pass

class MetaplacePluginManager:
    def __init__(self, plugins: Iterable[MetaplacePlugin] = ()) -> None:
        self.logger = logging.getLogger('metaplace.plugins')
        self._plugins: list[MetaplacePlugin] = []
        self._command_handlers: dict[str, CommandHandler] = {}

        for plugin in plugins:
            self.register(plugin)

    @property
    def plugins(self) -> tuple[MetaplacePlugin, ...]:
        return tuple(self._plugins)

    def register(self, plugin: MetaplacePlugin) -> None:
        handlers = plugin.command_handlers()
        duplicates = self._command_handlers.keys() & handlers.keys()

        if duplicates:
            commands = ', '.join(sorted(duplicates))
            raise ValueError(f'Metaplace commands already registered: {commands}')

        self._plugins.append(plugin)
        self._command_handlers.update(handlers)

    def on_connected(self, protocol: 'MetaplaceProtocol') -> None:
        for plugin in self._plugins:
            plugin.on_connected(protocol)

    def on_disconnected(self, protocol: 'MetaplaceProtocol') -> None:
        for plugin in reversed(self._plugins):
            plugin.on_disconnected(protocol)

    def on_player_ready(self, protocol: 'MetaplaceProtocol', player: 'GameObject') -> None:
        for plugin in self._plugins:
            plugin.on_player_ready(protocol, player)

    def dispatch(self, protocol: 'MetaplaceProtocol', command: Command) -> bool:
        handler = self._command_handlers.get(command.name)

        if handler is None:
            self.logger.debug('Unsupported command %s', command.name)
            return False

        handler(protocol, command)
        return True
