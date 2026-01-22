from app.domain.entities.post import Post
from app.domain.repositories.post_repository import PostRepository
from app.infrastructure.mappers.post_mapper import PostMapper
from app.infrastructure.models.post import PostModel
from app.infrastructure.repositories.sqlalchemy.base import SQLAlchemyRepository


class SQLAlchemyPostRepository(
    SQLAlchemyRepository[PostModel, Post],
    PostRepository,
):
    model = PostModel
    mapper = PostMapper()
