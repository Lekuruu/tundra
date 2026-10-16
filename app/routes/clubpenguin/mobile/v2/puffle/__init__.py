
from fastapi import APIRouter

from . import leashed

router = APIRouter()
router.include_router(leashed.router)
