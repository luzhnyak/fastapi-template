from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_category_service, get_current_user
from app.domain.entities.user import User
from app.schemas.category import (
    CategoryCreateRequest,
    CategoryListResponse,
    CategoryResponse,
    CategoryUpdateRequest,
)
from app.schemas.common import MAX_SQLITE_INTEGER, EntityId
from app.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=CategoryListResponse)
async def get_categories(
    skip: int = Query(0, ge=0, le=MAX_SQLITE_INTEGER),
    limit: int = Query(10, ge=1, le=100),
    service: CategoryService = Depends(get_category_service),
):
    return await service.get_categories(skip, limit)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: EntityId, service: CategoryService = Depends(get_category_service)
):
    return await service.get_category_by_id_or_404(category_id)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreateRequest,
    service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_user),
):
    return await service.create_category(data, current_user)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: EntityId,
    data: CategoryUpdateRequest,
    service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_user),
):
    return await service.update_category(category_id, data, current_user)


@router.delete("/{category_id}")
async def delete_category(
    category_id: EntityId,
    service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_user),
):
    category = await service.delete_category(category_id, current_user)
    return {"detail": f"Category {category.name} deleted"}
