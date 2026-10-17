
from sqlalchemy.orm import Session
from ..postgres import Login

def fetch_by_id(session: Session, id: int) -> Login | None:
    return session.query(Login) \
        .filter(Login.id == id) \
        .first()

def fetch_all(session: Session, penguin_id: int) -> list[Login]:
    return session.query(Login) \
        .filter(Login.penguin_id == penguin_id) \
        .all()

def fetch_many(
    session: Session,
    penguin_id: int,
    limit: int,
    offset: int,
) -> list[Login]:
    return session.query(Login) \
        .filter(Login.penguin_id == penguin_id) \
        .order_by(Login.id.desc()) \
        .limit(limit) \
        .offset(offset) \
        .all()

def fetch_by_ip(session: Session, ip_hash: str) -> list[Login]:
    return session.query(Login) \
        .filter(Login.ip_hash == ip_hash) \
        .all()

def fetch_recent(session: Session, penguin_id: int) -> Login | None:
    return session.query(Login) \
        .filter(Login.penguin_id == penguin_id) \
        .order_by(Login.id.desc()) \
        .first()

def add(
    session: Session,
    penguin_id: int,
    ip_hash: str,
) -> Login:
    login = Login(penguin_id=penguin_id, ip_hash=ip_hash)
    session.add(login)
    session.commit()
    return login

def update(
    session: Session,
    id: int,
    updates: dict,
) -> None:
    session.query(Login) \
        .filter(Login.id == id) \
        .update(updates)
    session.commit()

def update_recent(
    session: Session,
    penguin_id: int,
    updates: dict,
) -> None:
    session.query(Login) \
        .filter(Login.penguin_id == penguin_id) \
        .order_by(Login.id.desc()) \
        .limit(1) \
        .update(updates)
    session.commit()
