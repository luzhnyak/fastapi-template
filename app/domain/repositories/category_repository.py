from abc import ABC, abstractmethod
from app.domain.entities.post import Category
from app.domain.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category], ABC):

    @abstractmethod
    async def exists_by_slug(self, slug: str, exclude_id: int | None = None) -> bool:
        pass
