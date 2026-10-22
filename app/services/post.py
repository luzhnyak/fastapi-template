from app.core.exceptions import NotFoundException
from app.domain.entities.post import Post, PostList
from app.domain.entities.user import User
from app.domain.repositories.post_repository import PostRepository
from app.schemas.post import PostRequest
from app.services.base import BaseService


class PostService(BaseService):
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    async def create_post(self, data: PostRequest, current_user: User) -> Post:
        self._check_permission(current_user)
        return await self.post_repo.add_one({**data.model_dump(), "user_id": current_user.id})

    async def get_posts(self, skip: int = 0, limit: int = 12) -> PostList:
        return PostList(
            items=await self.post_repo.find_many(skip=skip, limit=limit),
            total=await self.post_repo.count_all(),
            page=skip // limit + 1,
            per_page=limit,
        )

    async def get_post_by_id(self, id: int) -> Post | None:
        return await self.post_repo.find_one(id=id)

    async def get_post_by_id_or_404(self, id: int) -> Post:
        post = await self.get_post_by_id(id)
        if post is None:
            raise NotFoundException(f"Post with id {id} not found")
        return post

    async def get_post_by_slug_or_404(self, slug: str) -> Post:
        post = await self.post_repo.find_one(slug=slug)
        if post is None:
            raise NotFoundException(f"Post with slug {slug} not found")
        return post

    async def update_post(self, post_id: int, data: PostRequest, current_user: User) -> Post:
        self._check_permission(current_user)
        await self.get_post_by_id_or_404(post_id)
        return await self.post_repo.edit_one(post_id, data.model_dump())

    async def delete_post(self, id: int, current_user: User) -> Post:
        self._check_permission(current_user)
        await self.get_post_by_id_or_404(id)
        return await self.post_repo.delete_one(id)
