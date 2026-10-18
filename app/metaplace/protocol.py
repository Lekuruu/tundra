
import logging
from collections.abc import Callable, Iterable

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineOnlyReceiver

from .plugin import MetaplacePlugin, MetaplacePluginManager
from .serialization import AllowedValues, Command, Tag
from .session import MetaplaceSession
from .world import World

CommandHandler = Callable[['MetaplaceProtocol', Command], bool | None]

class MetaplaceProtocol(LineOnlyReceiver):
    delimiter = b'\n'
    factory: "MetaplaceProtocolFactory"
    MAX_LENGTH = 5 * 1024

    def connectionMade(self) -> None:
        self.logger = logging.getLogger('metaplace.protocol')
        self.session = MetaplaceSession(self.factory.world, self.send_tag)
        self.user_agent = ''
        self.player_name = ''
        self.place_ready = False
        self.logger.info('Metaplace client connected from %s', self.transport.getPeer()) # type: ignore
        self.factory.plugins.on_connected(self)

    def lineReceived(self, line: bytes) -> None:
        try:
            command = Command.decode(line)
        except (UnicodeDecodeError, ValueError):
            self.close_connection()
            return

        self.logger.debug('-> %r', command)

        if not self.factory.command_handler(self, command):
            self.factory.plugins.dispatch(self, command)

    def sendTag(self, tag: Tag | str, *arguments: AllowedValues) -> None:
        message = tag if isinstance(tag, Tag) else Tag(tag, arguments)
        encoded = message.encode()
        self.transport.write(encoded) # type: ignore
        self.logger.debug('<- %r', message)

    def connectionLost(self, reason=None) -> None:
        if not hasattr(self, 'session'):
            # TODO: debug logging or sumthjing
            return

        self.logger.info('Metaplace player %s disconnected', self.session.player_id)
        try:
            self.factory.plugins.on_disconnected(self)
        finally:
            self.session.close()

    # i like snake_case more, sorry
    def send_tag(self, tag: Tag | str, *arguments: AllowedValues) -> None:
        return self.sendTag(tag, *arguments)

    def close_connection(self) -> None:
        self.transport.loseConnection() # type: ignore

class MetaplaceProtocolFactory(Factory):
    protocol = MetaplaceProtocol

    def __init__(
        self,
        world: World,
        command_handler: CommandHandler | None = None,
        plugins: Iterable[MetaplacePlugin] = (),
    ) -> None:
        self.world = world
        self.command_handler = command_handler or self.command_handler_stub
        self.plugins = MetaplacePluginManager(plugins)

    @staticmethod
    def command_handler_stub(protocol: MetaplaceProtocol, command: Command) -> bool:
        return False
