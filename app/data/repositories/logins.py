
from __future__ import annotations

from sqlalchemy.orm import Session
from typing import List

from .wrapper import session_wrapper
from ..objects import Login

@session_wrapper
def fetch_by_id(id: int, session: Session = ...) -> Login | None:
    return session.query(Login) \
        .filter(Login.id == id) \
        .first()

@session_wrapper
def fetch_all(penguin_id: int, session: Session = ...) -> List[Login]:
    return session.query(Login) \
        .filter(Login.penguin_id == penguin_id) \
        .all()

@session_wrapper
def fetch_many(
    penguin_id: int,
    limit: int,
    offset: int,
    session: Session = ...
) -> List[Login]:
    return session.query(Login) \
        .filter(Login.penguin_id == penguin_id) \
        .order_by(Login.id.desc()) \
        .limit(limit) \
        .offset(offset) \
        .all()

@session_wrapper
def fetch_by_ip(ip_hash: str, session: Session = ...) -> List[Login]:
    return session.query(Login) \
        .filter(Login.ip_hash == ip_hash) \
        .all()

@session_wrapper
def fetch_recent(penguin_id: int, session: Session = ...) -> Login | None:
    return session.query(Login) \
        .filter(Login.penguin_id == penguin_id) \
        .order_by(Login.id.desc()) \
        .first()

@session_wrapper
def add(
    penguin_id: int,
    ip_hash: str,
    session: Session = ...
) -> Login:
    login = Login(penguin_id=penguin_id, ip_hash=ip_hash)
    session.add(login)
    session.commit()
    return login

@session_wrapper
def update(
    id: int,
    updates: dict,
    session: Session = ...
) -> None:
    session.query(Login) \
        .filter(Login.id == id) \
        .update(updates)
    session.commit()

@session_wrapper
def update_recent(
    penguin_id: int,
    updates: dict,
    session: Session = ...
) -> None:
    session.query(Login) \
        .filter(Login.penguin_id == penguin_id) \
        .order_by(Login.id.desc()) \
        .limit(1) \
        .update(updates)
    session.commit()