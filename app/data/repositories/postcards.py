
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from .wrapper import SessionProvider, session_wrapper
from ..postgres import Postcard

@session_wrapper
def fetch_by_id(postcard_id: int, session: Session = SessionProvider) -> Postcard | None:
    return session.query(Postcard) \
        .filter(Postcard.id == postcard_id) \
        .first()

@session_wrapper
def fetch_all(session: Session = SessionProvider) -> List[Postcard]:
    return session.query(Postcard) \
        .all()
