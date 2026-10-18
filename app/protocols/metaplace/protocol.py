
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet.protocol import Factory
from collections.abc import Callable

from .serialization import AllowedValues, Command, Tag
from .session import MetaplaceSession
from .world import World

import logging

CommandHandler = Callable[['MetaplaceProtocol', Command], None]

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

    def lineReceived(self, line: bytes) -> None:
        try:
            command = Command.decode(line)
        except (UnicodeDecodeError, ValueError):
            self.close_connection()
            return

        self.logger.debug('Received metaplace command %s', command.name)
        self.factory.command_handler(self, command)

    def sendTag(self, tag: Tag | str, *arguments: AllowedValues) -> None:
        message = tag if isinstance(tag, Tag) else Tag(tag, arguments)
        self.transport.write(message.encode()) # type: ignore
        self.logger.debug('Sent metaplace tag %s', message.name)

    def connectionLost(self, reason=None) -> None:
        if hasattr(self, 'session'):
            self.logger.info('Metaplace player %s disconnected', self.session.player_id)
            self.session.close()

    # i like snake_case more, sorry
    def send_tag(self, tag: Tag | str, *arguments: AllowedValues) -> None:
        return self.sendTag(tag, *arguments)

    def close_connection(self) -> None:
        self.transport.loseConnection() # type: ignore

class MetaplaceProtocolFactory(Factory):
    protocol = MetaplaceProtocol

    def __init__(self, world: World, command_handler: CommandHandler | None = None) -> None:
        self.world = world
        self.command_handler = command_handler or self.command_handler_stub

    @staticmethod
    def command_handler_stub(protocol: MetaplaceProtocol, command: Command) -> None:
        pass
