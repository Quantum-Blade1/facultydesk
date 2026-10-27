import hashlib
import secrets
from datetime import timedelta
from typing import Any
from uuid import uuid4

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.clock import Clock, SystemClock
from app.core.config import get_settings

settings = get_settings()
_hasher = PasswordHasher()
_default_clock = SystemClock()


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(hash_value: str, password: str) -> bool:
    try:
        return _hasher.verify(hash_value, password)
    except VerifyMismatchError:
        return False


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(32)


def hash_refresh_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def create_access_token(
    subject: str,
    role: str,
    department_id: str | None = None,
    expires_delta: timedelta | None = None,
    clock: Clock | None = None,
) -> str:
    current_clock = clock or _default_clock
    now = current_clock.now()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "dept": department_id,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "jti": uuid4().hex,
        "type": "access",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
