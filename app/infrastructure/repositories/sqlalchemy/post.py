from sqlalchemy import select

from app.core.exceptions import ValidationException
from app.domain.entities.post import Post
from app.domain.repositories.post_repository import PostRepository
from app.infrastructure.mappers.post_mapper import PostMapper
from app.infrastructure.models.post import CategoryModel, PostModel, PostStatsModel
from app.infrastructure.repositories.sqlalchemy.base import SQLAlchemyRepository


class SQLAlchemyPostRepository(SQLAlchemyRepository[PostModel, Post], PostRepository):
    model = PostModel
    mapper = PostMapper()

    async def _categories(self, ids: list[int]) -> list[CategoryModel]:
        ids = set(ids)
        categories = list(
            (
                await self.session.scalars(select(CategoryModel).where(CategoryModel.id.in_(ids)))
            ).all()
        )
        if len(categories) != len(ids):
            raise ValidationException("One or more categories do not exist")
        return categories

    async def add_one(self, data: dict) -> Post:
        data = data.copy()
        data["categories"] = await self._categories(data.pop("category_ids", []))
        data["stats"] = PostStatsModel()
        return await super().add_one(data)

    async def edit_one(self, id: int, data: dict) -> Post:
        data = data.copy()
        if "category_ids" in data:
            data["categories"] = await self._categories(data.pop("category_ids"))
        return await super().edit_one(id, data)
