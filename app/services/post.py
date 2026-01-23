from passlib.context import CryptContext

from app.core.exceptions import (
    BadRequestException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
)

from app.domain.entities.post import Post, PostList
from app.infrastructure.repositories.sqlalchemy.post import PostRepository
from app.schemas.post import PostRequest
from app.services.base import BaseService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PostService(BaseService):
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    async def create_post(self, data: PostRequest, current_user_id: int) -> Post:
        self._check_permission(current_user_id)
        new_post = await self.post_repo.add_one(data)
        return new_post

    async def get_posts(self, skip: int = 0, limit: int = 12) -> PostList:
        total = await self.post_repo.count_all()
        page = (skip // limit) + 1
        posts = await self.post_repo.find_many_with_stats(skip=skip, limit=limit)
        return PostList(
            items=posts,
            total=total,
            page=page,
            per_page=limit,
        )

    async def get_post_by_id(self, id: int) -> Post | None:
        post = await self.post_repo.find_one_with_stats(id=id)
        if not post:
            return None
        return post

    async def get_post_by_id_or_404(self, id: int) -> Post:
        post = await self.post_repo.find_one_with_stats(id=id)
        if not post:
            raise NotFoundException(f"Post with id {id} not found")
        return post

    async def get_post_by_slug_or_404(self, slug: str) -> Post:
        post = await self.post_repo.find_one_with_stats(slug=slug)
        if not post:
            raise NotFoundException(f"Post with slug {slug} not found")
        return post

    async def update_post(
        self, post_id: int, data: PostRequest, current_user_id: int
    ) -> Post:
        self._check_permission(current_user_id)
        await self.get_post_by_id_or_404(post_id)
        updated_post = await self.post_repo.edit_one(post_id, data)
        return updated_post

    async def delete_post(self, id: int, current_user_id: int) -> Post:
        self._check_permission(current_user_id)
        await self.get_post_by_id_or_404(id)
        delete_post = await self.post_repo.delete_one(id=id)
        return delete_post
