
from __future__ import annotations
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from .wrapper import session_wrapper
from ..postgres import Postcard

@session_wrapper
def fetch_by_id(postcard_id: int, session: Session = ...) -> Postcard | None:
    return session.query(Postcard) \
        .filter(Postcard.id == postcard_id) \
        .first()

@session_wrapper
def fetch_all(penguin_id: int, session: Session = ...) -> List[Postcard]:
    return session.query(Postcard) \
        .all()
