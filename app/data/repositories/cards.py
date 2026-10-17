
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..postgres import Card, PenguinCard

def fetch_one(session: Session, id: int) -> Card | None:
    return session.query(Card) \
        .filter(Card.id == id) \
        .first()

def fetch_all(session: Session) -> list[Card]:
    return session.query(Card) \
        .all()

def fetch_by_element(session: Session, element: str) -> list[Card]:
    return session.query(Card) \
        .filter(Card.element == element) \
        .all()

def fetch_power_cards(session: Session) -> list[Card]:
    return session.query(Card) \
        .filter(Card.power_id > 0) \
        .all()

def fetch_by_penguin_id(
    session: Session,
    penguin_id: int,
    element: str,
) -> list[Card]:
    return session.query(Card) \
        .join(PenguinCard) \
        .filter(PenguinCard.penguin_id == penguin_id) \
        .filter(Card.element == element) \
        .all()

def fetch_power_cards_by_penguin_id(
    session: Session,
    penguin_id: int,
    element: str,
) -> list[Card]:
    # Subquery to generate series of cards, based on quantity
    subquery = session.query(
            PenguinCard.card_id,
            func.generate_series(1, PenguinCard.quantity).label("index"),
        ) \
        .filter(PenguinCard.penguin_id == penguin_id) \
        .subquery()

    return session.query(Card) \
        .join(subquery, Card.id == subquery.c.card_id) \
        .filter(Card.element == element) \
        .filter(Card.power_id > 0) \
        .all()

def fetch_count(
    session: Session,
    penguin_id: int,
    element: str,
) -> int:
    return session.query(func.sum(PenguinCard.quantity)) \
        .join(Card) \
        .filter(PenguinCard.penguin_id == penguin_id) \
        .filter(Card.element == element) \
        .scalar() or 0

def fetch_power_card_count(
    session: Session,
    penguin_id: int,
    element: str,
) -> int:
    return session.query(func.sum(PenguinCard.quantity)) \
        .join(Card) \
        .filter(PenguinCard.penguin_id == penguin_id) \
        .filter(Card.element == element) \
        .filter(Card.power_id > 0) \
        .scalar() or 0
