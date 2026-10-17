
from sqlalchemy.orm import Session
from ..postgres import PenguinPostcard

def create(session: Session, data: dict) -> PenguinPostcard:
    postcard = PenguinPostcard(**data)
    session.add(postcard)
    session.commit()
    return postcard

def fetch_by_id(session: Session, mail_id: int) -> PenguinPostcard | None:
    return session.query(PenguinPostcard) \
        .filter(PenguinPostcard.id == mail_id) \
        .first()

def fetch_all(session: Session, penguin_id: int) -> list[PenguinPostcard]:
    return session.query(PenguinPostcard) \
        .filter(PenguinPostcard.penguin_id == penguin_id) \
        .all()

def fetch_unread(session: Session, penguin_id: int) -> list[PenguinPostcard]:
    return session.query(PenguinPostcard) \
        .filter(PenguinPostcard.penguin_id == penguin_id) \
        .filter(PenguinPostcard.has_read == False) \
        .all()
