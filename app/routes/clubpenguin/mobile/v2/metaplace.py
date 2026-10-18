
from typing import Annotated

from fastapi import APIRouter, Query, Request
from starlette.authentication import requires

from app import security
from app.data import Penguin, SystemLanguage
from app.models import MPTokenResponse

router = APIRouter()

@router.get('/mpSessionToken', response_model=MPTokenResponse)
@requires('authenticated')
def mp_session_token(
    request: Request,
    language: Annotated[SystemLanguage, Query()],
    product: Annotated[str, Query()],
) -> MPTokenResponse:
    # TODO: Use same format as dash perhaps ?
    user: Penguin = request.user
    return MPTokenResponse(mpSessionToken=security.generate_token(user))
