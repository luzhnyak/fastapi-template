from app.domain.entities.comment import Comment
from app.domain.repositories.comment_repository import CommentRepository
from app.infrastructure.mappers.comment_mapper import CommentMapper
from app.infrastructure.models.comment import CommentModel
from app.infrastructure.repositories.sqlalchemy.base import SQLAlchemyRepository


class SQLAlchemyCommentRepository(SQLAlchemyRepository[CommentModel, Comment], CommentRepository):
    model = CommentModel
    mapper = CommentMapper()

    async def get_comments(self, skip: int = 0, limit: int = 12, **filter_by):
        return await self.find_many(skip=skip, limit=limit, **filter_by)
