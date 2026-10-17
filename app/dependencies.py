
from fastapi import Depends, Request
from collections.abc import Iterator
from sqlalchemy.orm import Session
from typing import Annotated

def database_session(request: Request) -> Iterator[Session]:
    with request.app.state.database.managed_session() as session:
        yield session

DatabaseSession = Annotated[Session, Depends(database_session)]
