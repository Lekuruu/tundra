
from __future__ import annotations
from pydantic import BaseModel

class Account(BaseModel):
    playerId: int
    playerSwid: str
    username: str
    email: str
    penguinAge: int
    colour: int
    language: int
    accountType: str
    member: bool
    lapsedMember: bool
    pendingActivation: bool
    safeMode: bool
    recurring: bool
    overrideType: str = ""
    daysLeft: int | None = None
    daysAsMember: int | None = None
    badgeLevel: int | None = None
    overriden: bool | None = None

class AuthData(BaseModel):
    playerId: int
    playerSwid: str
    username: str
    email: str
    displayName: str
    authToken: str
    friendsToken: str
    lastLogin: str
    member: bool
    pendingActivation: bool
    saveMode: bool
    accountType: str
    daysLeft: int | None = None
    recurring: bool = False
    overriden: bool = False
    overrideType: str | None = None
    consecutiveLoginCount: int = 0

class Identity(BaseModel):
    playerId: int
    playerSwid: str
    displayName: str
    accountType: str
    daysLeft: int
    badgeLevel: int
    member: bool
    username: str

class PlayerCardData(BaseModel):
    name: str
    coins: int
    daysAsMember: int
    badgeLevel: int
    totalLikesReceived: int
    totalLikesGiven: int
    remainingAwardGames: int
    penguinAge: int
    items: dict
    outfits: list
    member: bool
