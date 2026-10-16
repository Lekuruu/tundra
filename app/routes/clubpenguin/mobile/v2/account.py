
from fastapi import APIRouter, HTTPException, Request
from starlette.authentication import requires

from app.data import Penguin, SystemLanguage
from app.models import Account

router = APIRouter()

@router.get('/account', response_model=Account, response_model_exclude_none=True)
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
        colour=user.color or -1,
        language=SystemLanguage.Unknown, # TODO
        accountType=user.account_type,
        member=user.is_member,
        lapsedMember=False, # TODO
        pendingActivation=(not user.active),
        safeMode=user.safe_chat,
        recurring=True, # TODO
        daysAsMember=30, # TODO
        badgeLevel=user.badge_level,
        overriden=False,
        daysLeft=(
            max(7 - user.penguin_age, 0)
            if not user.active else -1
        )
    )

@router.put('/account')
def account_create(request: Request):
    raise HTTPException(501, 'Account creation is not implemented')
