
from __future__ import annotations
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..objects import PenguinPostcard
from .wrapper import session_wrapper

@session_wrapper
def fetch_by_id(mail_id: int, session: Session = ...) -> PenguinPostcard | None:
    return session.query(PenguinPostcard) \
        .filter(PenguinPostcard.id == mail_id) \
        .first()

@session_wrapper
def fetch_all(penguin_id: int, session: Session = ...) -> List[PenguinPostcard]:
    return session.query(PenguinPostcard) \
        .filter(PenguinPostcard.penguin_id == penguin_id) \
        .all()

@session_wrapper
def fetch_unread(penguin_id: int, session: Session = ...) -> List[PenguinPostcard]:
    return session.query(PenguinPostcard) \
        .filter(PenguinPostcard.penguin_id == penguin_id) \
        .filter(PenguinPostcard.has_read == False) \
        .all()
