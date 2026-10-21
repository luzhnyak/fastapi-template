from app.core.exceptions import ForbiddenException, NotFoundException
from app.domain.entities.comment import Comment, CommentList
from app.domain.entities.user import User
from app.domain.repositories.comment_repository import CommentRepository
from app.domain.repositories.post_repository import PostRepository
from app.schemas.comment import CommentCreateRequest, CommentUpdateRequest
from app.services.base import BaseService


class CommentService(BaseService):
    def __init__(self, comment_repo: CommentRepository, post_repo: PostRepository):
        self.comment_repo = comment_repo
        self.post_repo = post_repo

    async def create_comment(self, data: CommentCreateRequest, current_user: User) -> Comment:
        if await self.post_repo.find_one(id=data.post_id) is None:
            raise NotFoundException("Post not found")
        return await self.comment_repo.add_one({**data.model_dump(), "user_id": current_user.id})

    async def get_comments_by_post_id(
        self, post_id: int, skip: int = 0, limit: int = 12
    ) -> CommentList:
        return CommentList(
            items=await self.comment_repo.find_many(post_id=post_id, skip=skip, limit=limit),
            total=await self.comment_repo.count_all(post_id=post_id),
            page=skip // limit + 1,
            per_page=limit,
        )

    async def get_comments_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 12
    ) -> CommentList:
        return CommentList(
            items=await self.comment_repo.find_many(user_id=user_id, skip=skip, limit=limit),
            total=await self.comment_repo.count_all(user_id=user_id),
            page=skip // limit + 1,
            per_page=limit,
        )

    async def get_comment_by_id(self, id: int) -> Comment | None:
        return await self.comment_repo.find_one(id=id)

    async def get_comment_by_id_or_404(self, id: int) -> Comment:
        comment = await self.get_comment_by_id(id)
        if comment is None:
            raise NotFoundException(f"Comment with id {id} not found")
        return comment

    def _check_owner(self, comment: Comment, user: User) -> None:
        if comment.user_id != user.id and user.role != "admin":
            raise ForbiddenException("You cannot modify this comment")

    async def update_comment(
        self, id: int, data: CommentUpdateRequest, current_user: User
    ) -> Comment:
        comment = await self.get_comment_by_id_or_404(id)
        self._check_owner(comment, current_user)
        return await self.comment_repo.edit_one(id, data.model_dump())

    async def delete_comment(self, id: int, current_user: User) -> Comment:
        comment = await self.get_comment_by_id_or_404(id)
        self._check_owner(comment, current_user)
        return await self.comment_repo.delete_one(id)
