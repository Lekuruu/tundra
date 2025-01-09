
from fastapi import HTTPException, APIRouter, Request, Query
from starlette.authentication import requires
from app.data import SystemLanguage, Penguin
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
    language: SystemLanguage = Query(...)
) -> Identity:
    user = penguins.fetch_by_id(id)
    display_name = f'P{user.id}'

    if not user:
        raise HTTPException(404, 'Penguin not found')

    if is_username_approved(user, language):
        user.display_name = user.display_name

    return Identity(
        PlayerId=user.id,
        PlayerSwid=user.nickname,
        DisplayName=display_name,
        AccountType='normal', # TODO
        DaysLeft=30, # TODO
        BadgeLevel=1, # TODO
        Member=True, # TODO
        Username=user.username
    )
