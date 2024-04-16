
from fastapi import APIRouter

from . import authentication

router = APIRouter()
router.include_router(authentication.router)
