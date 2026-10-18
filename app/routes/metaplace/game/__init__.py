from fastapi import APIRouter

from . import wns

router = APIRouter()
router.include_router(wns.router, prefix='/get/world-name-service')
