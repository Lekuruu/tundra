
from starlette.authentication import requires
from fastapi import APIRouter, Request
from datetime import datetime

from app.data import Penguin, logins
from app.models import AuthData
from app import crypto

router = APIRouter()

@router.get('/authToken')
@requires('authenticated')
def authtoken_request(request: Request):
    user: Penguin = request.user

    # Default login time
    recent_login = datetime.now()

    # Fetch recent login time
    if (login := logins.fetch_recent(user.id)):
        recent_login = login.date

    return AuthData(
        PlayerId=user.id,
        PlayerSwid=user.nickname,
        Username=user.username,
        DisplayName=user.display_name,
        AuthToken=crypto.generate_token(user),
        LastLogin=recent_login.strftime('%Y-%m-%d %H:%M:%S'),
        SaveMode=user.safe_chat,
        Member=True, # TODO
        AccountType='normal', # TODO
        PendingActivation=(not user.active),
        DaysLeft=(
            max(7 - (datetime.now() - user.registration_date).days, 0)
            if not user.active else None
        )
    )
