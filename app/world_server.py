
from app.world import BASE_ASSET_URL, CLIENT_VERSION, create_place_presentation, create_world
from app.metaplace import BasicCommandHandler, MetaplaceProtocolFactory, MetaplaceWorldServer
from app.metaplace.plugins import CompanionAppPlugin
from app import security

import config

def authenticate_player(server_type: str, player_id: int, token: str) -> str | None:
    if server_type.lower() != 'live':
        return None

    token_data = security.decode_token(token)

    if token_data is None or token_data.get('id') != player_id:
        return None

    return str(token_data.get('name', ''))

def create_world_server() -> MetaplaceWorldServer:
    world = create_world()
    command_handler = BasicCommandHandler(
        world,
        authenticate_player,
        create_place_presentation(),
        version=CLIENT_VERSION,
        base_asset_url=BASE_ASSET_URL,
    )
    return MetaplaceWorldServer(
        MetaplaceProtocolFactory(
            world,
            command_handler,
            [CompanionAppPlugin()],
        ),
        config.METAPLACE_PORT,
        config.METAPLACE_BIND_HOST,
    )
