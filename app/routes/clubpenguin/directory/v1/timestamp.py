
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get('/timestamp')
def timestamp() -> dict:
    return {"timestamp": datetime.now().timestamp()}
