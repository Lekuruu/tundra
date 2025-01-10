
from fastapi.responses import RedirectResponse, Response
from fastapi import APIRouter, Request
from app.data import penguins

import config

router = APIRouter()

@router.get("/v1/{user_id}/cp")
def avatar_renderer_redirect(
    user_id: int,
    request: Request
) -> RedirectResponse:
    return RedirectResponse(
        url=f"{config.PLAY_BASEURL}/avatar/{user_id}/cp?{request.url.query}",
    )
