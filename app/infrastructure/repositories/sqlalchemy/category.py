from sqlalchemy import select
from app.domain.repositories.category_repository import CategoryRepository
from app.infrastructure.repositories.sqlalchemy.article import (
    SQLAlchemyArticleRepository,
)

from app.infrastructure.models.post import CategoryModel
from app.infrastructure.mappers.category_mapper import CategoryMapper
from app.domain.entities.post import Category


class SQLAlchemyCategoryRepository(
    SQLAlchemyArticleRepository[CategoryModel, Category],
    CategoryRepository,
):
    model = CategoryModel
    mapper = CategoryMapper()

    async def exists_by_slug(self, slug: str, exclude_id: int | None = None) -> bool:
        stmp = select(self.model).filter_by(slug=slug)
        if exclude_id:
            stmp = stmp.filter(self.model.id != exclude_id)

        res = await self.session.execute(stmp)
        return res.scalar_one_or_none() is not None
