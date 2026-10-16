
from fastapi import APIRouter
from time import time_ns

router = APIRouter()

@router.get('/timestamp')
def timestamp() -> dict:
    return {"timestamp": time_ns() // 1_000_000}
