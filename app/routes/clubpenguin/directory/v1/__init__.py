
from fastapi import APIRouter

from . import timestamp
from . import services
from . import mp

router = APIRouter()
router.include_router(timestamp.router)
router.include_router(services.router)
