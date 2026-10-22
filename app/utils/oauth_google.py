import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.core.exceptions import UnauthorizedException


async def get_user_info(code: str) -> dict:
    config = settings.app
    if not all((config.OAUTH_CLIENT_ID, config.OAUTH_SECRET, config.OAUTH_REDIRECT_URI)):
        raise HTTPException(status_code=503, detail="Google login is not configured")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": config.OAUTH_CLIENT_ID,
                    "client_secret": config.OAUTH_SECRET,
                    "redirect_uri": config.OAUTH_REDIRECT_URI,
                    "grant_type": "authorization_code",
                    "code": code,
                },
            )
            response.raise_for_status()
            token_data = response.json()
            token = token_data.get("access_token") if isinstance(token_data, dict) else None
            if not token:
                raise UnauthorizedException("Invalid Google authorization code")
            response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            info = response.json()
            if (
                not isinstance(info, dict)
                or info.get("verified_email") is not True
                or not info.get("email")
                or not isinstance(info.get("id"), str)
                or not info["id"]
            ):
                raise UnauthorizedException("A verified Google email is required")
            return info
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code < 500:
            raise UnauthorizedException("Invalid Google authorization") from None
        raise HTTPException(status_code=502, detail="Google login is unavailable") from None
    except (httpx.RequestError, ValueError):
        raise HTTPException(status_code=502, detail="Google login is unavailable") from None
