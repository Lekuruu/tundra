
from fastapi import APIRouter

from . import authentication
from . import playercard
from . import metaplace
from . import identity
from . import account
from . import puffle
from . import world

router = APIRouter()
router.include_router(authentication.router)
router.include_router(playercard.router)
router.include_router(identity.router)
router.include_router(account.router)
router.include_router(metaplace.router)
router.include_router(puffle.router, prefix='/puffle')
router.include_router(world.router, prefix='/world')
