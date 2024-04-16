
from app.data import Penguin
from typing import Union

from secrets import token_hex
from hashlib import md5

import config
import time
import jwt

def generate_random_key():
    return token_hex(8)

def generate_token(user: Penguin) -> str:
    return jwt.encode(
        {
            'sub': user.id,
            'name': user.username,
            'iat': round(time.time()),
        },
        config.STATIC_KEY,
        algorithm='HS256'
    )

def decode_token(token: str) -> dict:
    data = jwt.decode(
        token,
        config.STATIC_KEY,
        algorithms=['HS256']
    )

    for field in ('sub', 'name', 'iat'):
        if field not in data:
            return

    # TODO: Token expiration
    return data

def get_hash(undigested: Union[str, int, bytes]) -> str:
    if type(undigested) == str:
        undigested = undigested.encode('utf-8')

    elif type(undigested) == int:
        undigested = str(undigested).encode('utf-8')

    return md5(undigested).hexdigest()

def encrypt_password(password: str, digest=True):
    if digest:
        password = get_hash(password)

    swapped_hash = password[16:32] + password[0:16]
    return swapped_hash

def get_login_hash(password: str, rndk: str):
    key = encrypt_password(password, False)
    key += rndk
    key += 'Y(02.>\'H}t":E1'
    login_hash = encrypt_password(key)
    return login_hash
