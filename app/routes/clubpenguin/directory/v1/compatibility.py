
from __future__ import annotations
from fastapi import APIRouter, Query
from app.data import CompatibilityStatus

router = APIRouter()

@router.get('/compatibility/{app_id}')
def compatibility(app_id: str, version: str = Query(...)) -> dict:
    # TODO: Check version for updates
    return {"Status": CompatibilityStatus.Updated}
