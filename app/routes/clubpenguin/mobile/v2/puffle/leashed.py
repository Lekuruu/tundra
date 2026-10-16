
from fastapi import APIRouter, Request
from starlette.authentication import requires

router = APIRouter()

@router.get('/leashed_puffle')
@requires('authenticated')
def leashed_puffle(request: Request):
    # empty json = "no leashed puffle"
    return {}
