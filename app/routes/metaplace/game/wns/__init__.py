from fastapi import APIRouter

from . import start_world

router = APIRouter()
router.include_router(start_world.router)
