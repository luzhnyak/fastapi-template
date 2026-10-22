from datetime import UTC, datetime, timedelta
from uuid import uuid4

from jose import JWTError, jwt

from app.core.config import settings


def _create_token(data: dict, token_type: str, lifetime: timedelta) -> str:
    now = datetime.now(UTC)
    payload = {**data, "iat": now, "exp": now + lifetime, "type": token_type, "jti": str(uuid4())}
    return jwt.encode(payload, settings.app.SECRET_KEY, algorithm=settings.app.ALGORITHM)


def create_access_token(data: dict) -> str:
    return _create_token(
        data, "access", timedelta(minutes=settings.app.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(data: dict) -> str:
    return _create_token(data, "refresh", timedelta(days=settings.app.REFRESH_TOKEN_EXPIRE_DAYS))


def verify_token(token: str, token_type: str) -> dict:
    if not isinstance(token, str) or not token:
        raise JWTError("Missing token")
    payload = jwt.decode(
        token,
        settings.app.SECRET_KEY,
        algorithms=[settings.app.ALGORITHM],
        options={"require_exp": True, "require_iat": True, "require_sub": True},
    )
    if (
        payload.get("type") != token_type
        or not isinstance(payload.get("sub"), str)
        or not payload["sub"]
    ):
        raise JWTError("Invalid token")
    return payload


def verify_access_token(token: str) -> dict:
    return verify_token(token, "access")
