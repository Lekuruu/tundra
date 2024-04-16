
from fastapi import APIRouter

from . import mobile

router = APIRouter()
router.include_router(mobile.router, prefix="/mobile")
