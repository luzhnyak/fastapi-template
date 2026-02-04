from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ServerException, UnauthorizedException
from app.core.jwt import verify_access_token

from app.infrastructure.repositories.sqlalchemy.comment import (
    SQLAlchemyCommentRepository,
)


from app.infrastructure.repositories.sqlalchemy.post import SQLAlchemyPostRepository
from app.infrastructure.repositories.sqlalchemy.user import SQLAlchemyUserRepository
from app.schemas.auth import AuthResponse
from app.services.auth import AuthService

from app.services.comment import CommentService

from app.infrastructure.database import get_db

from app.services.post import PostService

from app.services.user import UserService


def get_post_repository(
    session: AsyncSession = Depends(get_db),
):
    return SQLAlchemyPostRepository(session)


def get_post_service(post_repo=Depends(get_post_repository)) -> PostService:
    return PostService(post_repo)


def get_comment_repository(
    session: AsyncSession = Depends(get_db),
):
    return SQLAlchemyCommentRepository(session)


def get_comment_service(
    comment_repo=Depends(get_comment_repository),
):
    return CommentService(comment_repo)


auth_token_schemas = HTTPBearer()


def get_user_repository(
    session: AsyncSession = Depends(get_db),
):
    return SQLAlchemyUserRepository(session)


def get_user_service(user_repo=Depends(get_user_repository)) -> UserService:
    return UserService(user_repo)


def get_auth_service(
    user_service=Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(auth_token_schemas),
    service: UserService = Depends(get_user_service),
) -> AuthResponse:
    try:
        payload = verify_access_token(token.credentials)
        email: str = payload.get("sub")
        if email is None:
            raise UnauthorizedException(detail="Invalid token")

        user = await service.get_user_by_email(email)
        print(user.avatar)
        return AuthResponse(
            access_token=token.credentials, token_type="Bearer", user=user
        )

    except JWTError:
        raise UnauthorizedException(detail="Invalid token")
    except Exception as e:
        raise ServerException(detail=str(e))
