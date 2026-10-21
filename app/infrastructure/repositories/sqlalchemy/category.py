from sqlalchemy import select

from app.domain.entities.post import Category
from app.domain.repositories.category_repository import CategoryRepository
from app.infrastructure.mappers.category_mapper import CategoryMapper
from app.infrastructure.models.post import CategoryModel
from app.infrastructure.repositories.sqlalchemy.base import SQLAlchemyRepository


class SQLAlchemyCategoryRepository(
    SQLAlchemyRepository[CategoryModel, Category], CategoryRepository
):
    model = CategoryModel
    mapper = CategoryMapper()

    async def exists_by_slug(self, slug: str, exclude_id: int | None = None) -> bool:
        stmt = select(self.model.id).where(self.model.slug == slug)
        if exclude_id is not None:
            stmt = stmt.where(self.model.id != exclude_id)
        return (await self.session.scalar(stmt)) is not None
