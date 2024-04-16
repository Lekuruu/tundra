
from fastapi import APIRouter

from . import v2

router = APIRouter()
router.include_router(v2.router, prefix="/v2")
