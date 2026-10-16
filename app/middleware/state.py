
from typing import Awaitable, Callable
from fastapi import Request

import app.session
import app

@app.api.middleware("http")
async def inject_database_state(request: Request, call_next: Callable) -> Awaitable:
    request.state.db = app.session.database
    return await call_next(request)
