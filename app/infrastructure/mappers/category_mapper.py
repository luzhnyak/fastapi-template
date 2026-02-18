from app.domain.entities.post import Category
from app.infrastructure.mappers.base import BaseMapper
from app.domain.entities.rating import Rating
from app.infrastructure.models.post import CategoryModel


class CategoryMapper(BaseMapper[CategoryModel, Category]):
    def to_entity(self, model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            slug=model.slug,
        )

    def to_model_dict(self, entity: Rating) -> dict:
        return {
            "name": entity.name,
            "slug": entity.slug,
        }
