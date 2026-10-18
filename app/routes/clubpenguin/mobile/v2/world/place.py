
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from starlette.authentication import requires
from typing import Annotated

router = APIRouter()

@router.get('/place/{place_name}', response_class=PlainTextResponse)
@requires('authenticated')
def world_name(
    request: Request,
    place_name: str,
    app_name: Annotated[str, Query(alias='appName')],
) -> str:
    resolved = request.app.state.world_catalog.resolve_place(app_name, place_name)
    if resolved is None:
        raise HTTPException(404, 'World place not found')

    world, _ = resolved
    return world.name
