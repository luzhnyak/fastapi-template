import secrets

from jose import JWTError
from starlette.concurrency import run_in_threadpool

from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.jwt import create_access_token, create_refresh_token, verify_token
from app.core.passwords import verify_password
from app.domain.entities.user import Auth, User
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.services.user import UserService
from app.utils.oauth_google import get_user_info


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def _authenticate(self, user: User) -> Auth:
        if not user.is_active:
            raise UnauthorizedException("Invalid credentials")
        return Auth(
            access_token=create_access_token({"sub": str(user.id)}),
            refresh_token=create_refresh_token({"sub": str(user.id)}),
            user=user,
        )

    async def register(self, data: RegisterRequest) -> Auth:
        return self._authenticate(await self.user_service.create_user(data))

    async def login(self, data: LoginRequest) -> Auth:
        user = await self.user_service.get_user_by_email(str(data.email))
        if not user or not await run_in_threadpool(verify_password, data.password, user.password):
            raise UnauthorizedException("Invalid credentials")
        return self._authenticate(user)

    async def google_login(self, code: str) -> Auth:
        info = await get_user_info(code)
        user = await self.user_service.get_user_by_google_id(info["id"])
        if user is None:
            if await self.user_service.get_user_by_email(info["email"]):
                raise ConflictException(
                    "Email already registered; sign in with your existing credentials"
                )
            user = await self.user_service.create_user(
                RegisterRequest(
                    name=info.get("name") or info["email"],
                    email=info["email"],
                    password=secrets.token_urlsafe(48),
                )
            )
            user = await self.user_service.bind_google_id(user.id, info["id"])
        return self._authenticate(user)

    async def refresh_token(self, refresh_token: str | None) -> Token:
        try:
            payload = verify_token(refresh_token, "refresh")
        except JWTError:
            raise UnauthorizedException("Invalid refresh token") from None
        try:
            user_id = int(payload["sub"])
        except ValueError:
            raise UnauthorizedException("Invalid refresh token") from None
        user = await self.user_service.get_user_by_id(user_id)
        if user is None or not user.is_active:
            raise UnauthorizedException("Invalid refresh token")
        auth = self._authenticate(user)
        return Token(access_token=auth.access_token, refresh_token=auth.refresh_token)
