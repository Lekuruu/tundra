
from fastapi import APIRouter

from . import place

router = APIRouter()
router.include_router(place.router)
