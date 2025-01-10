
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
            'id': user.id,
            'name': user.username,
            'exp': round(time.time()) + config.WEB_TOKEN_EXPIRATION,
        },
        config.STATIC_KEY,
        algorithm='HS256'
    )

def decode_token(token: str) -> dict:
    try:
        data = jwt.decode(
            token,
            config.STATIC_KEY,
            algorithms=['HS256']
        )
    except jwt.PyJWTError:
        return

    # Check if the token is expired
    if data['exp'] < round(time.time()):
        return

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
