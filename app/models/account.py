
from __future__ import annotations
from pydantic import BaseModel

class Account(BaseModel):
    PlayerId: int
    PlayerSwid: str
    Username: str
    Email: str
    PenguinAge: int
    Colour: int
    Language: int
    AccountType: str
    Member: bool
    LapsedMember: bool
    PendingActivation: bool
    SafeMode: bool
    Recurring: bool
    OverrideType: str = ""
    DaysLeft: int | None = None
    DaysAsMember: int | None = None
    BadgeLevel: int | None = None
    Overriden: bool | None = None

class AuthData(BaseModel):
    PlayerId: int
    PlayerSwid: str
    Username: str
    DisplayName: str
    AuthToken: str
    LastLogin: str
    Member: bool
    PendingActivation: bool
    SaveMode: bool
    AccountType: str
    DaysLeft: int | None = None

class Identity(BaseModel):
    PlayerId: int
    PlayerSwid: str
    DisplayName: str
    AccountType: str
    DaysLeft: int
    BadgeLevel: int
    Member: bool
    Username: str

class PlayerCardData(BaseModel):
    Name: str
    Coins: int
    DaysAsMember: int
    BadgeLevel: int
    TotalLikesReceived: int
    TotalLikesGiven: int
    RemainingAwardGames: int
    PenguinAge: int
    Items: dict
    Outfits: list
    Member: bool
