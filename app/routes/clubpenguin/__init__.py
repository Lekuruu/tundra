
from fastapi import APIRouter

from . import paperdoll
from . import directory
from . import mobile

router = APIRouter()
router.include_router(paperdoll.router, prefix="/paperdoll-renderer")
router.include_router(directory.router, prefix="/directory")
router.include_router(mobile.router, prefix="/mobile")
