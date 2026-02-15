from app.core.exceptions import (
    NotFoundException,
)

from app.domain.entities.post import Category, CategoryList
from app.domain.repositories.category_repository import CategoryRepository

from app.schemas.category import CategoryCreateRequest
from app.services.base import BaseService
from app.utils.transliterate import transliterate


class CategoryService(BaseService):
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def generate_unique_slug(
        self, title: str, exclude_id: int | None = None
    ) -> str:
        base_slug = transliterate(title)
        slug = base_slug
        counter = 1

        while await self.category_repo.exists_by_slug(slug, exclude_id=exclude_id):
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    async def create_category(
        self, data: CategoryCreateRequest, current_user_id: int
    ) -> Category:
        self._check_permission(current_user_id)
        new_post = await self.category_repo.add_one(data)
        return new_post

    async def get_categories(self, skip: int = 0, limit: int = 10) -> CategoryList:
        total = await self.category_repo.count_all()
        page = (skip // limit) + 1
        posts = await self.category_repo.find_many(skip=skip, limit=limit)
        return CategoryList(
            items=posts,
            total=total,
            page=page,
            per_page=limit,
        )

    async def get_category_by_id(self, id: int) -> Category | None:
        category = await self.category_repo.find_one(id=id)
        if not category:
            return None
        return category

    async def get_category_by_id_or_404(self, id: int) -> Category:
        category = await self.get_category_by_id(id)
        if not category:
            raise NotFoundException(f"Category with id {id} not found")
        return category

    async def get_category_by_slug_or_404(self, slug: str) -> Category:
        category = await self.category_repo.find_one_with_stats(slug=slug)
        if not category:
            raise NotFoundException(f"Category with slug {slug} not found")
        return category

    async def update_category(
        self, category_id: int, data: CategoryCreateRequest, current_user_id: int
    ) -> Category:
        self._check_permission(current_user_id)
        await self.get_category_by_id_or_404(category_id)
        updated_category = await self.category_repo.edit_one(category_id, data)
        return updated_category

    async def delete_category(self, id: int, current_user_id: int) -> Category:
        self._check_permission(current_user_id)
        await self.get_category_by_id_or_404(id)
        delete_category = await self.category_repo.delete_one(id=id)
        return delete_category
