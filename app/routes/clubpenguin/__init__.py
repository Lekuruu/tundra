
from fastapi import APIRouter

from . import directory
from . import mobile

router = APIRouter()
router.include_router(directory.router, prefix="/directory")
router.include_router(mobile.router, prefix="/mobile")
