
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis import Redis

import config
from app.data.postgres import Postgres
from app.routes import router as BaseRouter

logging.basicConfig(
    format='[%(asctime)s] - <%(name)s> %(levelname)s: %(message)s',
    level=logging.DEBUG if config.DEBUG else logging.INFO,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Postgres(
        config.POSTGRES_USER,
        config.POSTGRES_DBNAME,
        config.POSTGRES_PASSWORD,
        config.POSTGRES_HOST,
        config.POSTGRES_PORT,
    )
    redis = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT
    )
    app.state.database = database
    app.state.redis = redis

    try:
        yield
    finally:
        try:
            redis.close()
        finally:
            database.close()

api = FastAPI(
    title='mobile-services',
    description='Web services for various club penguin apps',
    openapi_url="/openapi.json" if config.DEBUG else None,
    redoc_url="/redoc" if config.DEBUG else None,
    docs_url="/docs" if config.DEBUG else None,
    debug=config.DEBUG,
    lifespan=lifespan,
)
api.include_router(BaseRouter)
