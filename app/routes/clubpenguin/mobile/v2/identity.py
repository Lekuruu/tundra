
from fastapi import APIRouter, HTTPException, Query, Request
from starlette.authentication import requires
from typing import Annotated

from app.data import Penguin, SystemLanguage
from app.data.repositories import penguins
from app.models import Identity

router = APIRouter()

def is_username_approved(penguin: Penguin, language: SystemLanguage) -> bool:
    supported_approval_languages = [
        "en", "pt", "fr", "es", "de", "ru", "tr"
    ]

    if language.code not in supported_approval_languages:
        return penguin.approval_en and not penguin.rejection_en

    approved = getattr(penguin, f'approval_{language.code}')
    rejected = getattr(penguin, f'rejection_{language.code}')
    return approved and not rejected

@router.get('/identity/{id}', response_model=Identity)
@requires('authenticated')
def identity(
    request: Request,
    id: int,
    language: Annotated[SystemLanguage, Query()]
) -> Identity:
    user = penguins.fetch_by_id(id)

    if not user:
        raise HTTPException(404, 'Penguin not found')

    username = f'P{user.id}'

    if is_username_approved(user, language):
        username = user.display_name

    return Identity(
        playerId=user.id,
        playerSwid=user.swid,
        displayName=user.username,
        username=username,
        accountType=user.account_type,
        daysLeft=(
            max(7 - user.penguin_age, 0)
            if not user.active else -1
        ),
        badgeLevel=user.badge_level,
        member=user.is_member
    )
