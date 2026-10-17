
from sqlalchemy.orm import Session
from ..postgres import Item, PenguinItem

def create(session: Session, data: dict) -> Item:
    item = Item(**data)
    session.add(item)
    session.commit()
    return item

def fetch_one(session: Session, id: int) -> Item | None:
    return session.query(Item) \
        .filter(Item.id == id) \
        .first()

def fetch_by_penguin_id(session: Session, penguin_id: int) -> list[Item]:
    return session.query(Item) \
        .join(PenguinItem, Item.id == PenguinItem.item_id) \
        .filter(PenguinItem.penguin_id == penguin_id) \
        .all()

def fetch_item_by_penguin_id(
    session: Session,
    penguin_id: int,
    item_id: int,
) -> Item | None:
    return session.query(Item) \
        .join(PenguinItem, Item.id == PenguinItem.item_id) \
        .filter(PenguinItem.penguin_id == penguin_id) \
        .filter(PenguinItem.item_id == item_id) \
        .first()

def add(
    session: Session,
    penguin_id: int,
    item_id: int,
) -> None:
    if item_exists(session, penguin_id, item_id):
        return

    session.add(PenguinItem(penguin_id=penguin_id, item_id=item_id))
    session.commit()

def remove(
    session: Session,
    penguin_id: int,
    item_id: int,
) -> None:
    session.query(PenguinItem) \
        .filter(PenguinItem.penguin_id == penguin_id) \
        .filter(PenguinItem.item_id == item_id) \
        .delete()
    session.commit()

def item_exists(
    session: Session,
    penguin_id: int,
    item_id: int,
) -> bool:
    return session.query(PenguinItem) \
        .filter(PenguinItem.penguin_id == penguin_id) \
        .filter(PenguinItem.item_id == item_id) \
        .count() > 0
