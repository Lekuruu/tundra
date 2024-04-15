
from app.data.postgres import Postgres

import config

database = Postgres(
    config.POSTGRES_USER,
    config.POSTGRES_DBNAME,
    config.POSTGRES_PASSWORD,
    config.POSTGRES_HOST,
    config.POSTGRES_PORT
)
