
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis import Redis

from app.data.postgres import Postgres
from app.world import create_world_catalog

import config

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
    app.state.world_catalog = create_world_catalog()

    try:
        yield
    finally:
        try:
            redis.close()
        finally:
            database.close()
