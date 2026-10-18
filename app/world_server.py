
from app import security
from app.world import create_place_presentation, create_world
from app.protocols.metaplace import (
    BasicCommandHandler,
    MetaplaceProtocolFactory,
    MetaplaceWorldServer,
)
import config

def create_world_server() -> MetaplaceWorldServer:
    world = create_world()
    command_handler = BasicCommandHandler(
        world,
        security.decode_token,
        create_place_presentation(),
    )
    return MetaplaceWorldServer(
        MetaplaceProtocolFactory(world, command_handler),
        config.METAPLACE_PORT,
        config.METAPLACE_BIND_HOST,
    )
