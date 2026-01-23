from passlib.context import CryptContext
from passlib.hash import sha256_crypt
from sqlalchemy.ext.asyncio import AsyncSession
import requests
from jose import ExpiredSignatureError, JWTError, jwt
from http import HTTPStatus

from app.core.exceptions import (
    BadRequestException,
    ConflictException,
    UnauthorizedException,
)
from app.domain.entities.user import Auth
from app.schemas.auth import Auth0Token, LoginRequest, RegisterRequest, Token
from app.schemas.user import SignInRequest, SignUpRequest
from app.core.jwt import create_access_token, create_refresh_token
from app.core.config import settings
from app.services.user import UserService
from app.utils.oauth_google import get_user_info

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return sha256_crypt.verify(plain_password, hashed_password)

    async def register(self, user_data: RegisterRequest) -> Auth:
        user = await self.user_service.get_user_by_email(user_data.email)
        if user:
            raise ConflictException("User with this email already exists")

        new_user = await self.user_service.create_user(user_data)

        access_token = create_access_token({"sub": new_user.email})
        refresh_token = create_refresh_token({"sub": new_user.email})

        return Auth(
            access_token=access_token, refresh_token=refresh_token, user=new_user
        )

    async def login(self, user_data: LoginRequest) -> Auth:
        user = await self.user_service.get_user_by_email(user_data.email)

        if not user or not self.verify_password(user_data.password, user.password):
            raise UnauthorizedException(detail="Invalid credentials")

        access_token = create_access_token({"sub": user.email})
        refresh_token = create_refresh_token({"sub": user.email})

        return Auth(access_token=access_token, refresh_token=refresh_token, user=user)

    async def google_login(self, code: str) -> Auth:
        user_social = get_user_info(
            code, f"{settings.app.BASE_URL_NEXT}/api/auth/google/callback"
        )

        print(user_social)
        if (
            user_social.get("error", None)
            and user_social.get("error").get("code") == 401
        ):
            raise BadRequestException(detail=user_social.get("error").get("message"))

        user = await self.user_service.get_user_by_email(user_social.get("email"))

        if not user:
            user_data = RegisterRequest(
                name=user_social.get("name"),
                email=user_social.get("email"),
                password=user_social.get("email"),
            )
            user = await self.user_service.create_user(user_data)
            # user.google_id = user_social.get("id")

        access_token = create_access_token({"sub": user.email})
        refresh_token = create_refresh_token({"sub": user.email})

        return Auth(access_token=access_token, refresh_token=refresh_token, user=user)

    async def refresh_token(self, refresh_token: str) -> Token:
        try:
            payload = jwt.decode(
                refresh_token,
                settings.app.SECRET_KEY,
                algorithms=[settings.app.ALGORITHM],
            )
            email = payload.get("sub")
            if email is None:
                raise UnauthorizedException(detail="Invalid refresh token")

            access_token = create_access_token({"sub": email})
            new_refresh_token = create_refresh_token({"sub": email})

            return Token(access_token=access_token, refresh_token=new_refresh_token)
        except ExpiredSignatureError:
            raise UnauthorizedException(detail="Refresh token expired")
        except JWTError:
            raise UnauthorizedException(detail="Invalid refresh token")
