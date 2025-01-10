
from starlette.authentication import requires
from fastapi import APIRouter, Request
from datetime import datetime

from app.data import Penguin, SystemLanguage
from app.models import Account

router = APIRouter()

@router.get('/account', response_model=Account)
@requires('authenticated')
def account(request: Request):
    user: Penguin = request.user

    return Account(
        playerId=user.id,
        playerSwid=user.swid,
        username=user.nickname,
        displayName=user.username,
        email=user.email,
        penguinAge=user.penguin_age,
        colour=user.color,
        language=SystemLanguage.Unknown, # TODO
        accountType=user.account_type,
        member=user.is_member,
        lapsedMember=False, # TODO
        pendingActivation=(not user.active),
        safeMode=user.safe_chat,
        recurring=True, # TODO
        daysAsMember=30, # TODO
        daysLeft=(
            max(7 - user.penguin_age, 0)
            if not user.active else None
        )
    )
