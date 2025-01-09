
from fastapi import APIRouter
from . import services

router = APIRouter()
router.include_router(services.router)
