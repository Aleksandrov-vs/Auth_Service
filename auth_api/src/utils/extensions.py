import datetime
import hashlib
import os
from flask_jwt_extended import (create_access_token,
                                create_refresh_token)


def create_tokens(
        identity: str,
        access_expires_delta: datetime.timedelta,
        refresh_expires_delta: datetime.timedelta = datetime.timedelta(days=2),
        additional_claims: dict | None = None
) -> tuple[str, str]:
    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims,
        expires_delta=access_expires_delta
    )
    refresh_token = create_refresh_token(
        identity=identity,
        expires_delta=refresh_expires_delta
    )
    return access_token, refresh_token


def create_hash(password: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    pass_hash = salt + b":" + key
    return str(pass_hash)
