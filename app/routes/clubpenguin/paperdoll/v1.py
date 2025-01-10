
from fastapi.responses import RedirectResponse, Response
from fastapi import APIRouter, Request
from app.data import penguins

import config

router = APIRouter()

@router.get("/v1/{username}/cp")
def avatar_renderer_redirect(
    username: str,
    request: Request
) -> RedirectResponse:
    user = penguins.fetch_by_name_case_insensitive(username)

    if not user:
        raise Response(status_code=404, content='')

    return RedirectResponse(
        url=f"{config.PLAY_BASEURL}/avatar/{user.id}/cp?{request.url.query}",
    )
