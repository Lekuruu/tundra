
from starlette.authentication import requires
from fastapi import APIRouter, Request
from datetime import datetime

from app.models import AuthData
from app.data import Penguin
from app import crypto

router = APIRouter()

@router.get('/authToken')
@requires('authenticated')
def authtoken_request(request: Request):
    user: Penguin = request.user

    return AuthData(
        PlayerId=user.id,
        PlayerSwid=user.nickname,
        Username=user.username,
        DisplayName=user.display_name,
        AuthToken=crypto.generate_token(user),
        LastLogin='lastlogin', # TODO
        Member=True, # TODO
        PendingActivation=(not user.active),
        SaveMode=user.safe_chat,
        AccountType='accounttype', # TODO
        DaysLeft=(
            max(7 - (datetime.now() - user.registration_date).days, 0)
            if not user.active else None
        )
    )
