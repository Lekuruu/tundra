from fastapi import APIRouter, Request
from redis import Redis
from starlette.authentication import requires

from app.data import Penguin, items, penguins
from app.api_dependencies import DatabaseSession
from app.models import Items, Outfit, OutfitPayload, PlayerCardData, PlayerCardOutfit

router = APIRouter()

@router.get("/card-data", response_model=PlayerCardData)
@requires("authenticated")
def player_card(
    request: Request,
    session: DatabaseSession,
) -> PlayerCardData:
    user: Penguin = request.user
    user_items = items.fetch_by_penguin_id(session, user.id)

    outfit = Outfit(
        colour=user.color or -1,
        head=user.head or -1,
        face=user.face or -1,
        neck=user.neck or -1,
        body=user.body or -1,
        hand=user.hand or -1,
        feet=user.feet or -1,
        flag=user.flag or -1,
        photo=user.photo or -1,
    )

    item_model = Items(
        COLOUR=[item.id for item in user_items if item.is_color()],
        HEAD=[item.id for item in user_items if item.is_head()],
        FACE=[item.id for item in user_items if item.is_face()],
        NECK=[item.id for item in user_items if item.is_neck()],
        BODY=[item.id for item in user_items if item.is_body()],
        HAND=[item.id for item in user_items if item.is_hand()],
        FEET=[item.id for item in user_items if item.is_feet()],
        FLAG=[item.id for item in user_items if item.is_flag()],
        PHOTO=[item.id for item in user_items if item.is_photo()],
        OTHER=[item.id for item in user_items if item.is_award()],
    )

    return PlayerCardData(
        name=user.display_name,
        coins=user.coins,
        member=user.is_member,
        badgeLevel=user.badge_level,
        daysAsMember=30,  # TODO
        totalLikesReceived=0,  # TODO
        totalLikesGiven=0,  # TODO
        remainingAwardGames=0,  # TODO
        penguinAge=user.penguin_age,
        items=item_model,
        outfits=[PlayerCardOutfit(itemList=outfit.serialize())],
    )

@router.put("/outfit", response_model=OutfitPayload)
@requires("authenticated")
def save_outfit(
    request: Request,
    payload: OutfitPayload,
    session: DatabaseSession,
) -> OutfitPayload:
    user: Penguin = request.user
    outfit = payload.outfit

    penguins.update(
        session,
        user.id,
        {
            "color": None if outfit.colour == -1 else outfit.colour,
            "head": None if outfit.head == -1 else outfit.head,
            "face": None if outfit.face == -1 else outfit.face,
            "neck": None if outfit.neck == -1 else outfit.neck,
            "body": None if outfit.body == -1 else outfit.body,
            "hand": None if outfit.hand == -1 else outfit.hand,
            "feet": None if outfit.feet == -1 else outfit.feet,
            "flag": None if outfit.flag == -1 else outfit.flag,
            "photo": None if outfit.photo == -1 else outfit.photo,
        },
    )

    redis: Redis = request.app.state.redis
    cache_keys = list(redis.scan_iter(match=f"{user.id}.*.avatar"))
    if cache_keys:
        redis.delete(*cache_keys)

    return OutfitPayload(outfit=outfit)
