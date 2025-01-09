
from __future__ import annotations
from fastapi import APIRouter, Query
import config

router = APIRouter()

@router.get('/services')
def services(product: str | None = Query(None)) -> dict:
    return {
        "appstore-sledracer": "http://itunes.apple.com/WebObjects/MZStore.woa/wa/viewSoftware?id=894932355",
        "appstore-pufflewild": "http://itunes.apple.com/WebObjects/MZStore.woa/wa/viewSoftware?id=767801968",
        "character-avatar-service": "http://media1.friends.go.com/images/CP",
        "igloo-renderer-service": "http://igloo.clubpenguin.com:80",
        "playdom-geopixel-service": "https://log.data.disney.com/g",
        "playdom-logging-service": "https://log.data.disney.com/cp",
        "friends-tigase-server": "friends.clubpenguin.com:5223",
        "avatar-renderer-service": "http://paperdoll.clubpenguin.com",
        "cpblog": f"{config.HOME_BASEURL}/%@blog?nochrome=1",
        "cpnewspaper": f"{config.HOME_BASEURL}/%@cpnewspaper",
        "cp_event-service": f"{config.API_BASEURL}/clubpenguin/mobile/v2",
        "message-service": f"{config.API_BASEURL}/clubpenguin/mobile/v2",
        "catalog-service": f"{config.API_BASEURL}/clubpenguin/mobile/v2",
        "avatar-renderer-service-cellophane": f"{config.API_BASEURL}/clubpenguin/paperdoll-renderer/v1",
        "player-data-service": f"{config.API_BASEURL}/clubpenguin/mobile/v2",
        "games-service": f"{config.API_BASEURL}/clubpenguin/mobile/v2",
        "apple-product-id-service": f"{config.API_BASEURL}/clubpenguin/mobile/v2",
        "catalog-items-images": f"{config.MEDIA8_BASEURL}/game/items/images/",
        "avatar-image-service_items": f"{config.MEDIA8_BASEURL}/game/items/images/paper/image",
        "login-service": f"{config.API_BASEURL}/clubpenguin/mobile/v2",
        "cp_ui_locfile": f"{config.MEDIA8_BASEURL}/mobile/localization/<version>/<locale_string>.json.gz",
        "game_config": f"{config.MEDIA8_BASEURL}/play/%@/web_service/game_configs/",
        "commerce-service": f"{config.API_BASEURL}/clubpenguin/mobile/v2",
        "account-service": f"{config.API_BASEURL}/clubpenguin/mobile/v2",
        "pc-baseurl-ac": f"{config.API_BASEURL}/social/autocomplete/v2/search",
        "rewards-service": f"{config.API_BASEURL}/clubpenguin/mobile/v2",
        "igloo-renderer-service-cellophane": f"{config.API_BASEURL}/clubpenguin/igloo-renderer/v1",
        "cp-mobile-services": f"{config.API_BASEURL}/clubpenguin/mobile/v2",
        "avatar-image-service": f"{config.MEDIA8_BASEURL}/game/items/images/paper",
        "avatar-image-service_icons": f"{config.MEDIA8_BASEURL}/game/items/images/paper/icon",
        "cp-baseurl-ui": f"{config.MEDIA8_BASEURL}/mobile/cp-mobile-ui/<locale_string>/deploy/metaplace/ipad2",
        "cjsnow_card_assets": f"{config.MEDIA8_BASEURL}/game/mpassets/minigames/cjsnow/en_US/deploy/png/ipad2/cards/",
        "cp-baseurl-ui-1.3": f"{config.MEDIA8_BASEURL}/mobile/cp-mobile-ui/v1_3/<locale_string>/deploy/metaplace/ipad2",
        "cdn-baseurl": f"{config.MEDIA8_BASEURL}/mobile/payloads",
        "cjsnow_assets": f"{config.MEDIA8_BASEURL}/game/mpassets/minigames/cjsnow/en_US/deploy",
        "cp-baseurl-ui-clubpenguin-1.5": f"{config.MEDIA8_BASEURL}/mobile/cp-mobile-ui/clubpenguin_v1_5/<locale_string>/deploy/metaplace/devicepng",
        "cp-baseurl-ui-clubpenguin-1.4": f"{config.MEDIA8_BASEURL}/mobile/cp-mobile-ui/clubpenguin_v1_4/<locale_string>/deploy/metaplace/ipad2",
        "catalog-image-service": f"{config.MEDIA8_BASEURL}/catalog",
        "game_config_v2": f"{config.MEDIA8_BASEURL}/play/<locale_string>/web_service/game_configs/",
        "avatar-image-service_photos": f"{config.MEDIA8_BASEURL}/game/items/images/paper/image"
    }
