
from app.routes import router as BaseRouter
from fastapi import FastAPI

import uvicorn
import logging
import config

logging.basicConfig(
    format='[%(asctime)s] - <%(name)s> %(levelname)s: %(message)s',
    level=logging.DEBUG if config.DEBUG else logging.INFO,
)

api = FastAPI(
    title='mobile-services',
    description='Web services for various club penguin apps',
    redoc_url=None,
    docs_url=None,
    debug=True if config.DEBUG else False
)

api.include_router(BaseRouter)

def run():
    uvicorn.run(
        api,
        host=config.WEB_HOST,
        port=config.WEB_PORT,
        log_config=None
    )
