

from fastapi import APIRouter, Query

router = APIRouter()

@router.get('/services')
def services(
    product: str = Query(...),
    version: str = Query(...),
    app_id: str = Query(..., alias='appId')
) -> dict:
    return {
        "base_asset_url": "http://media8.clubpenguin.com/mobile/",
        "manifest_url": "http://media8.clubpenguin.com/mobile/publishdata/r6519/manifest/manifest_tokenized.json",
        "version": "1.2.0",
        "version_requested": "1.2.0",
        "wns": "http://n7vcp1clubpwns.clubpenguin.com:80/",
        "wns_product": "clubpenguin"
    }
