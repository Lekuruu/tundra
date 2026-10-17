
from collections.abc import Callable
from typing import TypeVar
from sqlalchemy.orm import Session
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    UnauthenticatedUser,
)

from app.data import CELLOPHANE_TOKENS, Penguin, penguins
from app import api, crypto

import asyncio
import config
import base64
import bcrypt

PenguinKey = TypeVar("PenguinKey")

class AuthBackend(AuthenticationBackend):
    async def authenticate(self, request: HTTPConnection):
        if not (authorization := request.headers.get("Authorization")):
            return

        authorizations = self.parse_authorization_header(authorization)

        if not (cello_token := authorizations.get("FD")):
            return

        if cello_token not in CELLOPHANE_TOKENS.values():
            return

        scopes = ["application"]

        if "Basic" not in authorizations:
            return AuthCredentials(scopes), UnauthenticatedUser()

        data, password = self.parse_basic_authentication(authorizations["Basic"])

        if not password:
            # No password was given, so we assume the data is a token
            user = await self.token_authentication(request, data)

        else:
            # Authenticate client using username & password
            user = await self.password_authentication(request, data, password)

        if not user:
            return AuthCredentials(scopes), UnauthenticatedUser()

        scopes.append("authenticated")

        if user.active:
            scopes.append("activated")

        if user.moderator:
            scopes.append("moderator")

        return AuthCredentials(scopes), user

    async def password_authentication(
        self,
        request: HTTPConnection,
        username: str,
        password: str,
    ) -> Penguin | None:
        penguin = await asyncio.to_thread(
            self.fetch_penguin,
            request,
            penguins.fetch_by_name_case_insensitive,
            username,
        )

        if not penguin:
            return

        login_hash = crypto.get_login_hash(
            crypto.get_hash(password).upper(),
            config.STATIC_KEY
        )

        password_correct = await asyncio.to_thread(
            bcrypt.checkpw,
            login_hash.encode("utf-8"),
            penguin.password.encode("utf-8")
        )

        if not password_correct:
            return

        return penguin

    async def token_authentication(
        self,
        request: HTTPConnection,
        token: str,
    ) -> Penguin | None:
        data = crypto.decode_token(token)

        if not data:
            return

        penguin = await asyncio.to_thread(
            self.fetch_penguin,
            request,
            penguins.fetch_by_id,
            data["id"],
        )

        if not penguin:
            return

        return penguin

    def parse_authorization_header(self, header: str) -> dict:
        try:
            return {
                key.strip(): value.strip()
                for key, value in (
                    method.strip().split(maxsplit=1)
                    for method in header.split(",")
                )
            }
        except ValueError:
            return {}

    def parse_basic_authentication(self, token: str) -> tuple[str, str]:
        username, password = base64.b64decode(token).decode().split(":", maxsplit=1)
        return username, password

    @staticmethod
    def fetch_penguin(
        request: HTTPConnection,
        fetch: Callable[[Session, PenguinKey], Penguin | None],
        key: PenguinKey,
    ) -> Penguin | None:
        with request.app.state.database.managed_session() as session:
            return fetch(session, key)

api.add_middleware(AuthenticationMiddleware, backend=AuthBackend())
