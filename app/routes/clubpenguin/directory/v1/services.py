
from __future__ import annotations
from fastapi import APIRouter, Query

router = APIRouter()

@router.get('/services')
def services(product: str | None = Query(None)) -> dict:
    return {
        "cpblog": "http://www.clubpenguin.com/%@blog?nochrome=1",
        "cp_event-service": "https://api.disney.com/clubpenguin/mobile/v2",
        "cdn-baseurl": "http://media8.clubpenguin.com/mobile/payloads",
        "appstore-sledracer": "http://itunes.apple.com/WebObjects/MZStore.woa/wa/viewSoftware?id=894932355",
        "catalog-service": "https://api.disney.com/clubpenguin/mobile/v2",
        "cjsnow_assets": "http://media8.clubpenguin.com/game/mpassets/minigames/cjsnow/en_US/deploy",
        "cp-baseurl-ui-clubpenguin-1.5": "http://media8.clubpenguin.com/mobile/cp-mobile-ui/clubpenguin_v1_5/<locale_string>/deploy/metaplace/devicepng",
        "igloo-renderer-service": "http://igloo.clubpenguin.com:80",
        "cp-baseurl-ui-clubpenguin-1.4": "http://media8.clubpenguin.com/mobile/cp-mobile-ui/clubpenguin_v1_4/<locale_string>/deploy/metaplace/ipad2",
        "message-service": "https://api.disney.com/clubpenguin/mobile/v2",
        "catalog-image-service": "http://media8.clubpenguin.com/catalog",
        "playdom-geopixel-service": "https://log.data.disney.com/g",
        "appstore-pufflewild": "http://itunes.apple.com/WebObjects/MZStore.woa/wa/viewSoftware?id=767801968",
        "game_config_v2": "http://media8.clubpenguin.com/play/<locale_string>/web_service/game_configs/",
        "avatar-image-service_photos": "http://media8.clubpenguin.com/game/items/images/paper/image",
        "avatar-renderer-service-cellophane": "https://api.disney.com/clubpenguin/paperdoll-renderer/v1",
        "player-data-service": "https://api.disney.com/clubpenguin/mobile/v2",
        "games-service": "https://api.disney.com/clubpenguin/mobile/v2",
        "character-avatar-service": "http://media1.friends.go.com/images/CP",
        "apple-product-id-service": "https://api.disney.com/clubpenguin/mobile/v2",
        "playdom-logging-service": "https://log.data.disney.com/cp",
        "catalog-items-images": "http://media8.clubpenguin.com/game/items/images/",
        "avatar-image-service_items": "http://media8.clubpenguin.com/game/items/images/paper/image",
        "login-service": "https://api.disney.com/clubpenguin/mobile/v2",
        "friends-tigase-server": "friends.clubpenguin.com:5223",
        "cp_ui_locfile": "http://media8.clubpenguin.com/mobile/localization/<version>/<locale_string>.json.gz",
        "game_config": "http://media8.clubpenguin.com/play/%@/web_service/game_configs/",
        "commerce-service": "https://api.disney.com/clubpenguin/mobile/v2",
        "avatar-renderer-service": "http://paperdoll.clubpenguin.com",
        "account-service": "https://api.disney.com/clubpenguin/mobile/v2",
        "pc-baseurl-ac": "https://api.disney.com/social/autocomplete/v2/search",
        "rewards-service": "https://api.disney.com/clubpenguin/mobile/v2",
        "igloo-renderer-service-cellophane": "https://api.disney.com/clubpenguin/igloo-renderer/v1",
        "cp-mobile-services": "https://api.disney.com/clubpenguin/mobile/v2",
        "avatar-image-service": "http://media8.clubpenguin.com/game/items/images/paper",
        "cpnewspaper": "http://www2.clubpenguin.com/%@cpnewspaper",
        "avatar-image-service_icons": "http://media8.clubpenguin.com/game/items/images/paper/icon",
        "cp-baseurl-ui": "http://media8.clubpenguin.com/mobile/cp-mobile-ui/<locale_string>/deploy/metaplace/ipad2",
        "cjsnow_card_assets": "http://media8.clubpenguin.com/game/mpassets/minigames/cjsnow/en_US/deploy/png/ipad2/cards/",
        "cp-baseurl-ui-1.3": "http://media8.clubpenguin.com/mobile/cp-mobile-ui/v1_3/<locale_string>/deploy/metaplace/ipad2"
    }
