from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.infrastructure.mappers.comment_mapper import CommentMapper
from app.infrastructure.models.comment import CommentModel
from app.domain.entities.comment import Comment

from app.domain.repositories.comment_repository import CommentRepository
from app.infrastructure.repositories.sqlalchemy.base import SQLAlchemyRepository


class SQLAlchemyCommentRepository(
    SQLAlchemyRepository[CommentModel, Comment],
    CommentRepository,
):
    model = CommentModel
    mapper = CommentMapper()

    async def get_comments(self, skip: int = 0, limit: int = 12, **filter_by):
        stmt = (
            select(self.model)
            .options(selectinload(self.model.user))
            .filter_by(**filter_by)
            .offset(skip)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        models = res.scalars().all()
        return [self.mapper.to_entity(m) for m in models]
