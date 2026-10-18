
from fastapi import APIRouter

from . import clubpenguin
from . import metaplace

router = APIRouter()
router.include_router(clubpenguin.router, prefix="/clubpenguin")
router.include_router(metaplace.router)
