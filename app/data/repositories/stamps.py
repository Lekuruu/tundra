
from sqlalchemy.orm import Session
from ..postgres import PenguinStamp, Stamp

def fetch_one(session: Session, id: int) -> Stamp | None:
    return session.query(Stamp) \
        .filter(Stamp.id == id) \
        .first()

def fetch_all_by_group(session: Session, group_id: int) -> list[Stamp]:
    return session.query(Stamp) \
        .filter(Stamp.group_id == group_id) \
        .all()

def fetch_by_penguin_id(
    session: Session,
    penguin_id: int,
    group_id: int | None = None,
) -> list[Stamp]:
    query = session.query(Stamp) \
        .join(PenguinStamp, Stamp.id == PenguinStamp.stamp_id) \
        .filter(PenguinStamp.penguin_id == penguin_id)

    if group_id:
        query = query.filter(Stamp.group_id == group_id)

    return query.all()

def add(
    session: Session,
    id: int,
    penguin_id: int,
) -> PenguinStamp:
    penguin_stamp = PenguinStamp(penguin_id=penguin_id, stamp_id=id)
    session.add(penguin_stamp)
    session.commit()
    return penguin_stamp

def remove(
    session: Session,
    id: int,
    penguin_id: int,
) -> int:
    rows = session.query(PenguinStamp) \
        .filter_by(penguin_id=penguin_id, stamp_id=id) \
        .delete()
    session.commit()
    return rows

def exists(
    session: Session,
    id: int,
    penguin_id: int,
) -> bool:
    return session.query(PenguinStamp) \
        .filter_by(penguin_id=penguin_id, stamp_id=id) \
        .count() > 0

def completed_group(
    session: Session,
    penguin_id: int,
    group_id: int,
) -> bool:
    total = session.query(Stamp) \
        .filter(Stamp.group_id == group_id) \
        .count()

    collected = session.query(Stamp) \
        .join(PenguinStamp, Stamp.id == PenguinStamp.stamp_id) \
        .filter(PenguinStamp.penguin_id == penguin_id) \
        .filter(Stamp.group_id == group_id) \
        .count()

    return total == collected
