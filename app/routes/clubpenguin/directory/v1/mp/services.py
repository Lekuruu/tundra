

from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

product_configurations = {
    "clubpenguin": {
        "base_asset_url": "http://media8.clubpenguin.com/mobile/",
        "manifest_url": "http://media8.clubpenguin.com/mobile/publishdata/r6519/manifest/manifest_tokenized.json",
        "wns": "http://n7vcp1clubpwns.clubpenguin.com:80/",
    },
    "cjsnow": {
        "base_asset_url": "http://media1.clubpenguin.com/game/mpassets/",
        "manifest_url": "http://media1.clubpenguin.com/game/mpassets/publishdata/r5309/manifest/manifest_tokenized.json",
        "wns": "http://n7vcp1clubpwns.clubpenguin.com:80/",
    }
}

@router.get('/services')
def services(
    product: str = Query(...),
    version: str = Query(...),
    app_id: str = Query(..., alias='appId')
) -> dict:
    config = product_configurations.get(product)

    if config is None:
        raise HTTPException(404, "Product not found")
    
    return {
        "base_asset_url": config["base_asset_url"],
        "manifest_url": config["manifest_url"],
        "version": "1.6.23",
        "version_requested": version,
        "wns": config["wns"],
        "wns_product": product
    }
