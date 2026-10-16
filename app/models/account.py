
from pydantic import BaseModel

from .items import Items


class Account(BaseModel):
    playerId: int
    playerSwid: str
    username: str
    displayName: str
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
    daysLeft: int = -1
    daysAsMember: int = -1
    badgeLevel: int = -1
    overriden: bool = False
    expirationTimestamp: float | None = None
    preactivPlayTime: float | None = None
    preactivGracePeriod: float | None = None


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
    safeMode: bool
    accountType: str
    daysLeft: int = -1
    recurring: bool = False
    overriden: bool = False
    overrideType: str = ""
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


class MPTokenResponse(BaseModel):
    mpSessionToken: str


class PlayerCardOutfit(BaseModel):
    itemList: str


class PlayerCardData(BaseModel):
    name: str
    coins: int
    daysAsMember: int
    badgeLevel: int
    totalLikesReceived: int
    totalLikesGiven: int
    remainingAwardGames: int
    penguinAge: int
    items: Items
    outfits: list[PlayerCardOutfit]
    member: bool
