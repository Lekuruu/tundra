
from fastapi import APIRouter

from . import clubpenguin

router = APIRouter()
router.include_router(clubpenguin.router, prefix="/clubpenguin")
