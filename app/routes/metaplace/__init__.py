from fastapi import APIRouter

from . import game

router = APIRouter()
router.include_router(game.router, prefix='/api/v0.2/xxx/game')
