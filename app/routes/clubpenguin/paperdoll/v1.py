
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request
import config

router = APIRouter()

@router.get("/v1/{user_id}/cp", response_class=RedirectResponse)
def avatar_renderer_redirect(
    user_id: int,
    request: Request
) -> RedirectResponse:
    return RedirectResponse(
        url=f"{config.PLAY_BASEURL}/avatar/{user_id}/cp?{request.url.query}",
    )
