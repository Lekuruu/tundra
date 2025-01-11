
from starlette.authentication import requires
from fastapi import APIRouter, Request
from app.models import PlayerCardData, Outfit, Items
from app.data import Penguin, items

router = APIRouter()

@router.get('/card-data', response_model=PlayerCardData)
@requires('authenticated')
def player_card(request: Request) -> PlayerCardData:
    user: Penguin = request.user
    user_items = items.fetch_by_penguin_id(user.id)

    outfit = Outfit(
        colour=user.color or -1,
        head=user.head or -1,
        face=user.face or -1,
        neck=user.neck or -1,
        body=user.body or -1,
        hand=user.hand or -1,
        feet=user.feet or -1,
        flag=user.flag or -1,
        photo=user.photo or -1
    )

    item_model = Items(
        colour=[item.id for item in user_items if item.is_color()],
        head=[item.id for item in user_items if item.is_head()],
        face=[item.id for item in user_items if item.is_face()],
        neck=[item.id for item in user_items if item.is_neck()],
        body=[item.id for item in user_items if item.is_body()],
        hand=[item.id for item in user_items if item.is_hand()],
        feet=[item.id for item in user_items if item.is_feet()],
        flag=[item.id for item in user_items if item.is_flag()],
        photo=[item.id for item in user_items if item.is_photo()],
        award=[item.id for item in user_items if item.is_award()]
    )

    return PlayerCardData(
        name=user.display_name,
        coins=user.coins,
        member=user.is_member,
        badgeLevel=user.badge_level,
        daysAsMember=30, # TODO
        totalLikesReceived=0, # TODO
        totalLikesGiven=0, # TODO
        remainingAwardGames=0, # TODO
        penguinAge=user.penguin_age,
        items=item_model,
        outfit=[outfit.serialize()]
    )
