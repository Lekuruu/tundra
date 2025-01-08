
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
        PlayerId=user.id,
        PlayerSwid=user.nickname,
        Username=user.username,
        DisplayName=user.display_name,
        Email=user.email,
        PenguinAge=(datetime.now() - user.registration_date).days,
        Colour=user.color,
        Language=SystemLanguage.Unknown, # TODO
        AccountType='normal', # TODO
        Member=True, # TODO
        LapsedMember=False, # TODO
        PendingActivation=(not user.active),
        SafeMode=user.safe_chat,
        Recurring=False, # TODO
        DaysAsMember=30, # TODO
        DaysLeft=(
            max(7 - (datetime.now() - user.registration_date).days, 0)
            if not user.active else None
        )
    )
