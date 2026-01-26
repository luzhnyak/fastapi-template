from fastapi import APIRouter, Depends, status
import logging

from app.api.dependencies import get_current_user, get_user_service
from app.schemas.user import (
    SignUpRequest,
    UserResponse,
    UserUpdateRequest,
    UsersListResponse,
)

from app.services.user import UserService


router = APIRouter(prefix="/users", tags=["Users"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: SignUpRequest,
    service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(get_current_user),
):
    user = await service.create_user(data, current_user.id)
    logger.info(f"User created: {user.name}")
    return user


@router.get("/", response_model=UsersListResponse)
async def get_users(
    skip: int = 0, limit: int = 10, service: UserService = Depends(get_user_service)
):
    return await service.get_users(skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int, service: UserService = Depends(get_user_service)
):
    user = await service.get_user_by_id_or_404(user_id)
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdateRequest,
    service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(get_current_user),
):
    updated_user = await service.update_user(user_id, user_data, current_user.id)
    logger.info(f"User updated: {updated_user.name}")
    return updated_user


@router.delete("/{id}")
async def delete_user(
    id: int,
    service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(get_current_user),
):
    deleted_user = await service.delete_user(id, current_user.id)
    logger.info(f"User deleted: {deleted_user.name}")
    return {"detail": f"User {deleted_user.name} deleted"}
