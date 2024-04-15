
from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..objects import BuddyList, BuddyRequest, IgnoreList
from .wrapper import session_wrapper

@session_wrapper
def fetch_buddy_list(penguin_id: int, session: Session = ...) -> BuddyList:
    return session.query(BuddyList) \
        .filter(BuddyList.penguin_id == penguin_id) \
        .first()

@session_wrapper
def fetch_buddy_requests(penguin_id: int, session: Session = ...) -> list[BuddyRequest]:
    return session.query(BuddyRequest) \
        .filter(BuddyRequest.penguin_id == penguin_id) \
        .all()

@session_wrapper
def fetch_ignore_list(penguin_id: int, session: Session = ...) -> list[BuddyList]:
    return session.query(IgnoreList) \
        .filter(IgnoreList.penguin_id == penguin_id) \
        .all()

@session_wrapper
def is_buddy(penguin_id: int, buddy_id: int, session: Session = ...) -> bool:
    return session.query(BuddyList) \
        .filter(BuddyList.penguin_id == penguin_id) \
        .filter(BuddyList.buddy_id == buddy_id) \
        .first() is not None

@session_wrapper
def is_best_buddy(penguin_id: int, buddy_id: int, session: Session = ...) -> bool:
    return session.query(BuddyList) \
        .filter(BuddyList.penguin_id == penguin_id) \
        .filter(BuddyList.buddy_id == buddy_id) \
        .filter(BuddyList.best_buddy == True) \
        .first() is not None

@session_wrapper
def has_sent_request(penguin_id: int, target_id: int, session: Session = ...) -> bool:
    return session.query(BuddyRequest) \
        .filter(BuddyRequest.penguin_id == penguin_id) \
        .filter(BuddyRequest.buddy_id == target_id) \
        .first() is not None

@session_wrapper
def has_ignored(penguin_id: int, target_id: int, session: Session = ...) -> bool:
    return session.query(IgnoreList) \
        .filter(IgnoreList.penguin_id == penguin_id) \
        .filter(IgnoreList.buddy_id == target_id) \
        .first() is not None

@session_wrapper
def add_buddy(penguin_id: int, buddy_id: int, session: Session = ...) -> None:
    buddy_list = BuddyList(penguin_id=penguin_id, buddy_id=buddy_id)
    session.add(buddy_list)
    session.commit()

@session_wrapper
def remove_buddy(penguin_id: int, buddy_id: int, session: Session = ...) -> None:
    session.query(BuddyList) \
        .filter(BuddyList.penguin_id == penguin_id) \
        .filter(BuddyList.buddy_id == buddy_id) \
        .delete()
    session.commit()

@session_wrapper
def add_request(penguin_id: int, buddy_id: int, session: Session = ...) -> None:
    request = BuddyRequest(penguin_id=penguin_id, buddy_id=buddy_id)
    session.add(request)
    session.commit()

@session_wrapper
def remove_request(penguin_id: int, buddy_id: int, session: Session = ...) -> None:
    session.query(BuddyRequest) \
        .filter(BuddyRequest.penguin_id == penguin_id) \
        .filter(BuddyRequest.buddy_id == buddy_id) \
        .delete()
    session.commit()

@session_wrapper
def add_ignore(penguin_id: int, buddy_id: int, session: Session = ...) -> None:
    ignore_list = IgnoreList(penguin_id=penguin_id, buddy_id=buddy_id)
    session.add(ignore_list)
    session.commit()
