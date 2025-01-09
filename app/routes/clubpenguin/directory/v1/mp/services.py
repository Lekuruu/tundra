

from fastapi import APIRouter, HTTPException, Query
import config

router = APIRouter()

product_configurations = {
    "clubpenguin": {
        "base_asset_url": f"{config.MEDIA8_BASEURL}/mobile/",
        "manifest_url": f"{config.MEDIA8_BASEURL}/mobile/publishdata/r6519/manifest/manifest_tokenized.json",
        "wns": config.WNS_URL,
    },
    "cjsnow": {
        "base_asset_url": f"{config.MEDIA1_BASEURL}/game/mpassets/",
        "manifest_url": f"{config.MEDIA1_BASEURL}/game/mpassets/publishdata/r5309/manifest/manifest_tokenized.json",
        "wns": config.WNS_URL,
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
