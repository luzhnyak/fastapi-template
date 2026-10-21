from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedException
from app.core.jwt import verify_access_token
from app.domain.entities.user import User
from app.infrastructure.db.database import get_db
from app.infrastructure.repositories.sqlalchemy.category import SQLAlchemyCategoryRepository
from app.infrastructure.repositories.sqlalchemy.comment import SQLAlchemyCommentRepository
from app.infrastructure.repositories.sqlalchemy.post import SQLAlchemyPostRepository
from app.infrastructure.repositories.sqlalchemy.user import SQLAlchemyUserRepository
from app.services.auth import AuthService
from app.services.category import CategoryService
from app.services.comment import CommentService
from app.services.post import PostService
from app.services.user import UserService


def get_post_repository(session: AsyncSession = Depends(get_db, scope="function")):
    return SQLAlchemyPostRepository(session)


def get_post_service(repo=Depends(get_post_repository)) -> PostService:
    return PostService(repo)


def get_category_repository(session: AsyncSession = Depends(get_db, scope="function")):
    return SQLAlchemyCategoryRepository(session)


def get_category_service(repo=Depends(get_category_repository)) -> CategoryService:
    return CategoryService(repo)


def get_comment_repository(session: AsyncSession = Depends(get_db, scope="function")):
    return SQLAlchemyCommentRepository(session)


def get_comment_service(
    repo=Depends(get_comment_repository), post_repo=Depends(get_post_repository)
) -> CommentService:
    return CommentService(repo, post_repo)


def get_user_repository(session: AsyncSession = Depends(get_db, scope="function")):
    return SQLAlchemyUserRepository(session)


def get_user_service(repo=Depends(get_user_repository)) -> UserService:
    return UserService(repo)


def get_auth_service(service=Depends(get_user_service)) -> AuthService:
    return AuthService(service)


auth_token_schema = HTTPBearer(auto_error=False)


async def get_current_user(
    token: HTTPAuthorizationCredentials | None = Depends(auth_token_schema),
    service: UserService = Depends(get_user_service),
) -> User:
    if token is None:
        raise UnauthorizedException("Authentication required")
    try:
        payload = verify_access_token(token.credentials)
    except JWTError:
        raise UnauthorizedException("Invalid token") from None
    try:
        user_id = int(payload["sub"])
    except ValueError:
        raise UnauthorizedException("Invalid token") from None
    user = await service.get_user_by_id(user_id)
    if user is None or not user.is_active:
        raise UnauthorizedException("Invalid token")
    return user
