
from starlette.authentication import requires
from fastapi import APIRouter, Request
from datetime import datetime

from app.data import Penguin, logins
from app.models import AuthData
from app import crypto

router = APIRouter()

@router.get('/authToken', response_model=AuthData)
@requires('authenticated')
def authtoken(request: Request):
    user: Penguin = request.user

    # Default login time
    recent_login = datetime.now()

    # Fetch recent login time
    if (login := logins.fetch_recent(user.id)):
        recent_login = login.date

    return AuthData(
        playerId=user.id,
        playerSwid=user.nickname,
        username=user.username,
        displayName=user.display_name,
        authToken=crypto.generate_token(user),
        lastLogin=recent_login.strftime('%Y-%m-%d %H:%M:%S'),
        saveMode=user.safe_chat,
        member=user.is_member,
        accountType=user.account_type,
        pendingActivation=(not user.active),
        daysLeft=(
            max(7 - (datetime.now() - user.registration_date).days, 0)
            if not user.active else None
        )
    )
