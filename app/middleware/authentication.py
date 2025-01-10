
from __future__ import annotations
from typing import Tuple

from starlette.authentication import AuthenticationBackend, AuthCredentials, UnauthenticatedUser
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection

from app.data import penguins, Penguin
from app.data import CELLOPHANE_TOKENS
from app import api

import app.crypto as crypto
import asyncio
import base64
import bcrypt
import config

class AuthBackend(AuthenticationBackend):
    async def authenticate(self, request: HTTPConnection):
        if not (authorization := request.headers.get('Authorization')):
            return

        authorizations = self.parse_authorization_header(
            authorization
        )

        if not (cello_token := authorizations.get('FD')):
            return

        if cello_token not in CELLOPHANE_TOKENS.values():
            return

        scopes = ['application']

        if 'Basic' not in authorizations:
            return AuthCredentials(scopes), UnauthenticatedUser()

        data, password = self.parse_basic_authentication(
            authorizations['Basic']
        )

        if not password:
            # No password was given, so we assume the data is a token
            user = await self.token_authentication(data)

        else:
            # Authenticate client using username & password
            user = await self.password_authentication(data, password)

        if not user:
            return AuthCredentials(scopes), UnauthenticatedUser()

        scopes.append('authenticated')

        if user.active:
            scopes.append('activated')

        if user.moderator:
            scopes.append('moderator')

        return AuthCredentials(scopes), user

    async def password_authentication(self, username: str, password: str) -> Penguin | None:
        loop = asyncio.get_event_loop()

        penguin = await loop.run_in_executor(
            None, penguins.fetch_by_nickname, username
        )

        if not penguin:
            return

        login_hash = crypto.get_login_hash(
            crypto.get_hash(password).upper(),
            config.STATIC_KEY
        )

        password_correct = loop.run_in_executor(
            None, bcrypt.checkpw,
            login_hash.encode('utf-8'),
            penguin.password.encode('utf-8')
        )

        if not password_correct:
            return

        return penguin

    async def token_authentication(self, token: str) -> Penguin | None:
        data = crypto.decode_token(token)

        if not data:
            return

        loop = asyncio.get_event_loop()

        penguin = await loop.run_in_executor(
            None, penguins.fetch_by_id, data['sub']
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
                    for method in header.split(',')
                )
            }
        except ValueError:
            return {}

    def parse_basic_authentication(self, token: str) -> Tuple[str, str]:
        return base64.b64decode(token).decode().split(':', maxsplit=1)

api.add_middleware(AuthenticationMiddleware, backend=AuthBackend())
