
from __future__ import annotations

from sqlalchemy.orm import Session
from typing import List

from .wrapper import session_wrapper
from ..postgres import Item, PenguinItem

@session_wrapper
def create(data: dict, session: Session = ...) -> Item:
    item = Item(**data)
    session.add(item)
    session.commit()
    return item

@session_wrapper
def fetch_one(id: int, session: Session = ...) -> Item | None:
    return session.query(Item) \
        .filter(Item.id == id) \
        .first()

@session_wrapper
def fetch_by_penguin_id(penguin_id: int, session: Session = ...) -> List[Item]:
    return session.query(Item) \
        .join(PenguinItem, Item.id == PenguinItem.item_id) \
        .filter(PenguinItem.penguin_id == penguin_id) \
        .all()

@session_wrapper
def fetch_item_by_penguin_id(
    penguin_id: int,
    item_id: int,
    session: Session = ...
) -> Item | None:
    return session.query(Item) \
        .join(PenguinItem, Item.id == PenguinItem.item_id) \
        .filter(PenguinItem.penguin_id == penguin_id) \
        .filter(PenguinItem.item_id == item_id) \
        .first()

@session_wrapper
def add(
    penguin_id: int,
    item_id: int,
    session: Session = ...
) -> None:
    if item_exists(penguin_id, item_id, session=session):
        return

    session.add(PenguinItem(penguin_id=penguin_id, item_id=item_id))
    session.commit()

@session_wrapper
def remove(
    penguin_id: int,
    item_id: int,
    session: Session = ...
) -> None:
    session.query(PenguinItem) \
        .filter(PenguinItem.penguin_id == penguin_id) \
        .filter(PenguinItem.item_id == item_id) \
        .delete()
    session.commit()

@session_wrapper
def item_exists(
    penguin_id: int,
    item_id: int,
    session: Session = ...
) -> bool:
    return session.query(PenguinItem) \
        .filter(PenguinItem.penguin_id == penguin_id) \
        .filter(PenguinItem.item_id == item_id) \
        .count() > 0
