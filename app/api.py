
from app.middleware.authentication import AuthBackend
from app.routes import router as BaseRouter
from app.api_lifespan import lifespan

from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi import FastAPI

import logging
import config

logging.basicConfig(
    format='[%(asctime)s] - <%(name)s> %(levelname)s: %(message)s',
    level=logging.DEBUG if config.DEBUG else logging.INFO,
)

api = FastAPI(
    title='mobile-services',
    description='Web services for various club penguin apps',
    openapi_url="/openapi.json" if config.DEBUG else None,
    redoc_url="/redoc" if config.DEBUG else None,
    docs_url="/docs" if config.DEBUG else None,
    debug=config.DEBUG,
    lifespan=lifespan,
)
api.add_middleware(AuthenticationMiddleware, backend=AuthBackend())
api.include_router(BaseRouter)
