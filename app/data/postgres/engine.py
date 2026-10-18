
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from contextlib import contextmanager
from collections.abc import Iterator
import logging

from .models import Base


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

        Base.metadata.create_all(bind=self.engine)

    @property
    def database_url(self) -> str:
        return f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}'

    @property
    def session(self) -> Session:
        return self.sessionmaker(bind=self.engine)

    @contextmanager
    def managed_session(self) -> Iterator[Session]:
        session = self.sessionmaker(bind=self.engine)
        try:
            yield session
        except SQLAlchemyError:
            self.logger.exception('Database transaction failed. Performing rollback...')
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def close(self) -> None:
        self.engine.dispose()
