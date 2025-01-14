
from fastapi import APIRouter

from . import authentication
from . import playercard
from . import identity
from . import account

router = APIRouter()
router.include_router(authentication.router)
router.include_router(playercard.router)
router.include_router(identity.router)
router.include_router(account.router)
