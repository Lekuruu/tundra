
from starlette.authentication import requires
from fastapi import APIRouter, Request
from app.models import PlayerCardData
from app.data import Penguin

router = APIRouter()

@router.get('/card-data', response_model=PlayerCardData)
@requires('authenticated')
def player_card(request: Request) -> PlayerCardData:
    user: Penguin = request.user

    return PlayerCardData(
        name=user.display_name,
        coins=user.coins,
        daysAsMember=30, # TODO
        badgeLevel=1, # TODO
        totalLikesReceived=0, # TODO
        totalLikesGiven=0, # TODO
        remainingAwardGames=0, # TODO
        penguinAge=user.penguin_age, # TODO
        items={}, # TODO
        outfits=[], # TODO
        member=True # TODO
    )
