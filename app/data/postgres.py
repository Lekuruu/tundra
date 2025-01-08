
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from contextlib import contextmanager

from .objects import Base

import logging

class Postgres:
    def __init__(
        self,
        username: str,
        database_name: str,
        password: str,
        host: str,
        port: int
    ) -> None:
        self.logger = logging.getLogger('postgres')
        self.database_name = database_name
        self.username = username
        self.password = password
        self.host = host
        self.port = port

        self.engine = create_engine(
            self.database_url,
            pool_pre_ping=True,
            pool_recycle=900,
            pool_timeout=5,
            echo_pool=None,
            echo=None
        )

        self.sessionmaker = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

        self.engine.dispose()
        Base.metadata.create_all(bind=self.engine)

    @property
    def database_url(self) -> str:
        return f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}'

    @property
    def session(self) -> Session:
        return self.sessionmaker(bind=self.engine)

    @contextmanager
    def managed_session(self):
        session = self.sessionmaker(bind=self.engine)
        try:
            yield session
        except Exception as e:
            self.logger.fatal(f'Transaction failed: {e}', exc_info=e)
            self.logger.fatal('Performing rollback...')
            session.rollback()
            raise
        finally:
            session.close()
