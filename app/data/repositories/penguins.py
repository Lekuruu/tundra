
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..postgres import Penguin

def create(session: Session, data: dict) -> Penguin:
    penguin = Penguin(**data)
    session.add(penguin)
    session.commit()
    return penguin

def fetch_by_id(session: Session, id: int) -> Penguin | None:
    return session.query(Penguin) \
        .filter(Penguin.id == id) \
        .first()

def fetch_by_name(session: Session, name: str) -> Penguin | None:
    return session.query(Penguin) \
        .filter(Penguin.username == name) \
        .first()

def fetch_by_name_case_insensitive(session: Session, name: str) -> Penguin | None:
    return session.query(Penguin) \
        .filter(Penguin.username.ilike(name)) \
        .first()

def fetch_by_nickname(session: Session, nickname: str) -> Penguin | None:
    return session.query(Penguin) \
        .filter(Penguin.nickname == nickname) \
        .first()

def fetch_random(session: Session) -> Penguin | None:
    return session.query(Penguin) \
        .order_by(func.random()) \
        .first()

def update(session: Session, id: int, updates: dict) -> int:
    rows = session.query(Penguin) \
        .filter(Penguin.id == id) \
        .update(updates)
    session.commit()
    return rows
