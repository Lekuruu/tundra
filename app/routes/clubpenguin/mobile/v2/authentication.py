from datetime import datetime

from fastapi import APIRouter, Request
from starlette.authentication import requires

from app import crypto
from app.data import Penguin, logins
from app.dependencies import DatabaseSession
from app.models import AuthData

router = APIRouter()

@router.get("/authToken", response_model=AuthData)
@requires("authenticated")
def authtoken(
    request: Request,
    session: DatabaseSession,
):
    user: Penguin = request.user

    # Default login time
    recent_login = datetime.now()

    # Fetch recent login time
    if login := logins.fetch_recent(session, user.id):
        recent_login = login.date

    # Generate new token
    token = crypto.generate_token(user)

    return AuthData(
        playerId=user.id,
        playerSwid=user.swid,
        username=user.nickname,
        displayName=user.username,
        email=user.email,
        authToken=token,
        friendsToken=token,
        lastLogin=recent_login.strftime("%Y-%m-%d %H:%M:%S"),
        safeMode=user.safe_chat,
        member=user.is_member,
        accountType=user.account_type,
        pendingActivation=(not user.active),
        daysLeft=(
            max(7 - (datetime.now() - user.registration_date).days, 0)
            if not user.active
            else -1
        ),
    )
