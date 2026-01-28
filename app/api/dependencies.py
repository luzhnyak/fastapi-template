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


def get_fish_repository(
    session: AsyncSession = Depends(get_db),
):
    return SQLAlchemyFishRepository(session)


def get_fish_slug_repository(
    session: AsyncSession = Depends(get_db),
):
    return SQLAlchemyFishSlugRepository(session)


def get_fish_service(
    fish_repo=Depends(get_fish_repository),
    fish_slug_repo=Depends(get_fish_slug_repository),
):
    return FishService(fish_repo, fish_slug_repo)


def get_river_repository(
    session: AsyncSession = Depends(get_db),
):
    return SQLAlchemyRiverRepository(session)


def get_river_service(
    river_repo=Depends(get_river_repository),
):
    return RiverService(river_repo)


def get_place_repository(
    session: AsyncSession = Depends(get_db),
):
    return SQLAlchemyPlaceRepository(session)


def get_place_service(place_repo=Depends(get_place_repository)) -> PlaceService:
    return PlaceService(place_repo)


def get_blog_repository(
    session: AsyncSession = Depends(get_db),
):
    return SQLAlchemyBlogRepository(session)


def get_blog_service(blog_repo=Depends(get_blog_repository)) -> BlogService:
    return BlogService(blog_repo)


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
    place_repo=Depends(get_place_repository),
):
    return CommentService(comment_repo, place_repo)


def get_main_repository(
    session: AsyncSession = Depends(get_db),
):
    return SQLAlchemyMainRepository(session)


def get_main_service(
    main_repo=Depends(get_main_repository),
    blog_service=Depends(get_blog_service),
    fish_service=Depends(get_fish_service),
    river_service=Depends(get_river_service),
    post_service=Depends(get_post_service),
    place_service=Depends(get_place_service),
):
    return MainService(
        main_repo,
        blog_service,
        fish_service,
        river_service,
        post_service,
        place_service,
    )


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


def get_rating_repository(
    session: AsyncSession = Depends(get_db),
):
    return SQLAlchemyRatingRepository(session)


def get_rating_service(
    rating_repo=Depends(get_rating_repository),
    place_service=Depends(get_place_service),
) -> RatingService:
    return RatingService(rating_repo, place_service)
