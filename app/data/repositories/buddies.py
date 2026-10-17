
from sqlalchemy.orm import Session
from ..postgres import BuddyList, BuddyRequest, IgnoreList

def fetch_buddy_list(session: Session, penguin_id: int) -> BuddyList | None:
    return session.query(BuddyList) \
        .filter(BuddyList.penguin_id == penguin_id) \
        .first()

def fetch_buddy_requests(session: Session, penguin_id: int) -> list[BuddyRequest]:
    return session.query(BuddyRequest) \
        .filter(BuddyRequest.penguin_id == penguin_id) \
        .all()

def fetch_ignore_list(session: Session, penguin_id: int) -> list[IgnoreList]:
    return session.query(IgnoreList) \
        .filter(IgnoreList.penguin_id == penguin_id) \
        .all()

def is_buddy(session: Session, penguin_id: int, buddy_id: int) -> bool:
    return session.query(BuddyList) \
        .filter(BuddyList.penguin_id == penguin_id) \
        .filter(BuddyList.buddy_id == buddy_id) \
        .first() is not None

def is_best_buddy(session: Session, penguin_id: int, buddy_id: int) -> bool:
    return session.query(BuddyList) \
        .filter(BuddyList.penguin_id == penguin_id) \
        .filter(BuddyList.buddy_id == buddy_id) \
        .filter(BuddyList.best_buddy == True) \
        .first() is not None

def has_sent_request(session: Session, penguin_id: int, target_id: int) -> bool:
    return session.query(BuddyRequest) \
        .filter(BuddyRequest.penguin_id == penguin_id) \
        .filter(BuddyRequest.requester_id == target_id) \
        .first() is not None

def has_ignored(session: Session, penguin_id: int, target_id: int) -> bool:
    return session.query(IgnoreList) \
        .filter(IgnoreList.penguin_id == penguin_id) \
        .filter(IgnoreList.ignore_id == target_id) \
        .first() is not None

def add_buddy(session: Session, penguin_id: int, buddy_id: int) -> None:
    buddy_list = BuddyList(penguin_id=penguin_id, buddy_id=buddy_id)
    session.add(buddy_list)
    session.commit()

def remove_buddy(session: Session, penguin_id: int, buddy_id: int) -> None:
    session.query(BuddyList) \
        .filter(BuddyList.penguin_id == penguin_id) \
        .filter(BuddyList.buddy_id == buddy_id) \
        .delete()
    session.commit()

def add_request(session: Session, penguin_id: int, buddy_id: int) -> None:
    request = BuddyRequest(penguin_id=penguin_id, buddy_id=buddy_id)
    session.add(request)
    session.commit()

def remove_request(session: Session, penguin_id: int, buddy_id: int) -> None:
    session.query(BuddyRequest) \
        .filter(BuddyRequest.penguin_id == penguin_id) \
        .filter(BuddyRequest.requester_id == buddy_id) \
        .delete()
    session.commit()

def add_ignore(session: Session, penguin_id: int, buddy_id: int) -> None:
    ignore_list = IgnoreList(penguin_id=penguin_id, buddy_id=buddy_id)
    session.add(ignore_list)
    session.commit()
