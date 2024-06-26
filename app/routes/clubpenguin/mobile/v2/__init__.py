
from fastapi import APIRouter

from . import authentication
from . import account

router = APIRouter()
router.include_router(authentication.router)
router.include_router(account.router)
