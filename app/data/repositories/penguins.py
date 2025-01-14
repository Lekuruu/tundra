
from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import func

from .wrapper import session_wrapper
from ..postgres import Penguin

@session_wrapper
def create(data: dict, session: Session = ...) -> Penguin:
    penguin = Penguin(**data)
    session.add(penguin)
    session.commit()
    return penguin

@session_wrapper
def fetch_by_id(id: int, session: Session = ...) -> Penguin | None:
    return session.query(Penguin) \
        .filter(Penguin.id == id) \
        .first()

@session_wrapper
def fetch_by_name(name: str, session: Session = ...) -> Penguin | None:
    return session.query(Penguin) \
        .filter(Penguin.username == name) \
        .first()

@session_wrapper
def fetch_by_name_case_insensitive(name: str, session: Session = ...) -> Penguin | None:
    return session.query(Penguin) \
        .filter(Penguin.username.ilike(name)) \
        .first()

@session_wrapper
def fetch_by_nickname(nickname: str, session: Session = ...) -> Penguin | None:
    return session.query(Penguin) \
        .filter(Penguin.nickname == nickname) \
        .first()

@session_wrapper
def fetch_random(session: Session = ...) -> Penguin | None:
    return session.query(Penguin) \
        .order_by(func.random()) \
        .first()

@session_wrapper
def update(id: int, updates: dict, session: Session = ...) -> int:
    rows = session.query(Penguin) \
        .filter(Penguin.id == id) \
        .update(updates)
    session.commit()
    return rows
