
from starlette.authentication import requires
from fastapi import APIRouter, Request
from app.models import PlayerCardData
from app.data import Penguin, items

router = APIRouter()

@router.get('/card-data', response_model=PlayerCardData)
@requires('authenticated')
def player_card(request: Request) -> PlayerCardData:
    user: Penguin = request.user

    user_items = items.fetch_ids_by_penguin_id(
        penguin_id=user.id,
        # session=request.state.db
    )

    return PlayerCardData(
        name=user.display_name,
        coins=user.coins,
        daysAsMember=30, # TODO
        badgeLevel=user.badge_level,
        totalLikesReceived=0, # TODO
        totalLikesGiven=0, # TODO
        remainingAwardGames=0, # TODO
        penguinAge=user.penguin_age,
        items=user_items,
        outfits={}, # TODO
        member=user.is_member
    )
