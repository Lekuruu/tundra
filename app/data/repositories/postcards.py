
from sqlalchemy.orm import Session
from ..postgres import Postcard

def fetch_by_id(session: Session, postcard_id: int) -> Postcard | None:
    return session.query(Postcard) \
        .filter(Postcard.id == postcard_id) \
        .first()

def fetch_all(session: Session) -> list[Postcard]:
    return session.query(Postcard) \
        .all()
