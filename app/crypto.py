
from typing import Union

from secrets import token_hex
from hashlib import md5

def generate_random_key():
    return token_hex(8)

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