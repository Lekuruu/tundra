
from app.routes import router as BaseRouter
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
    redoc_url="/redoc" if config.DEBUG else None,
    docs_url="/docs" if config.DEBUG else None,
    debug=config.DEBUG
)

api.include_router(BaseRouter)
