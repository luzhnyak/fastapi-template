from app.core.exceptions import BadRequestException, NotFoundException
from app.domain.entities.post import Category, CategoryList
from app.domain.entities.user import User
from app.domain.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreateRequest, CategoryUpdateRequest
from app.services.base import BaseService


class CategoryService(BaseService):
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def create_category(self, data: CategoryCreateRequest, current_user: User) -> Category:
        self._check_permission(current_user)
        return await self.category_repo.add_one(data.model_dump())

    async def get_categories(self, skip: int = 0, limit: int = 10) -> CategoryList:
        return CategoryList(
            items=await self.category_repo.find_many(skip=skip, limit=limit),
            total=await self.category_repo.count_all(),
            page=skip // limit + 1,
            per_page=limit,
        )

    async def get_category_by_id(self, id: int) -> Category | None:
        return await self.category_repo.find_one(id=id)

    async def get_category_by_id_or_404(self, id: int) -> Category:
        category = await self.get_category_by_id(id)
        if category is None:
            raise NotFoundException(f"Category with id {id} not found")
        return category

    async def get_category_by_slug_or_404(self, slug: str) -> Category:
        category = await self.category_repo.find_one(slug=slug)
        if category is None:
            raise NotFoundException(f"Category with slug {slug} not found")
        return category

    async def update_category(
        self, category_id: int, data: CategoryUpdateRequest, current_user: User
    ) -> Category:
        self._check_permission(current_user)
        await self.get_category_by_id_or_404(category_id)
        updates = data.model_dump(exclude_none=True)
        if not updates:
            raise BadRequestException("No fields provided for update")
        return await self.category_repo.edit_one(category_id, updates)

    async def delete_category(self, id: int, current_user: User) -> Category:
        self._check_permission(current_user)
        await self.get_category_by_id_or_404(id)
        return await self.category_repo.delete_one(id)
