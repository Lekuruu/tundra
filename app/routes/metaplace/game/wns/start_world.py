from typing import Annotated

from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse

import config
from app import security
from app.protocols.metaplace import World

router = APIRouter()

@router.get('/start_world_request', response_class=PlainTextResponse)
def start_world_request(
    request: Request,
    name: Annotated[str | None, Query()] = None,
    product_name: Annotated[str | None, Query()] = None,
    owner: Annotated[str | None, Query()] = None,
    token: Annotated[str | None, Query()] = None,
) -> PlainTextResponse:
    if not name or not product_name or not owner or not token:
        return error_response(3518, 'Missing parameters')

    if product_name != 'clubpenguin':
        return error_response(3514, 'World type not supported')

    world = request.app.state.world_catalog.get_world(name)
    if world is None:
        return error_response(3514, 'World type not supported')
    if not owner.isdecimal():
        return error_response(3518, 'Invalid parameters')

    token_data = security.decode_token(token)
    if token_data is None:
        return error_response(3525, 'Invalid token')

    if (player_id := token_data.get("id")) is None:
        return error_response(3525, 'Invalid token')

    if int(player_id) != int(owner):
        return error_response(3525, 'Invalid token')

    return world_response(world)

def world_response(world: World) -> PlainTextResponse:
    fields = (
        '[S_WORLDLIST]',
        world.world_id,
        world.name,
        config.METAPLACE_HOST,
        config.METAPLACE_PORT,
        '',
        world.owner,
        world.clean_name or world.name,
        'CPNext_dev_branch',
        'example',
    )
    return PlainTextResponse(
        '|'.join(str(field) for field in fields),
        headers={'Cache-Control': 'no-store'},
    )

def error_response(code: int, message: str) -> PlainTextResponse:
    return PlainTextResponse(
        f'[S_ERROR]|{code}|Cannot Start World|{message}',
        headers={'Cache-Control': 'no-store'},
    )
