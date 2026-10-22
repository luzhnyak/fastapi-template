from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_current_user, get_user_service
from app.domain.entities.user import User
from app.schemas.common import MAX_SQLITE_INTEGER, EntityId
from app.schemas.user import SignUpRequest, UserResponse, UsersListResponse, UserUpdateRequest
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: SignUpRequest,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    service._check_permission(current_user)
    return await service.create_user(data)


@router.get("/", response_model=UsersListResponse)
async def get_users(
    skip: int = Query(0, ge=0, le=MAX_SQLITE_INTEGER),
    limit: int = Query(10, ge=1, le=100),
    service: UserService = Depends(get_user_service),
):
    return await service.get_users(skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: EntityId, service: UserService = Depends(get_user_service)):
    return await service.get_user_by_id_or_404(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: EntityId,
    data: UserUpdateRequest,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return await service.update_user(user_id, data, current_user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: EntityId,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    user = await service.delete_user(user_id, current_user)
    return {"detail": f"User {user.name} deleted"}
