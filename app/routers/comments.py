from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_comment_service, get_current_user
from app.domain.entities.user import User
from app.schemas.comment import (
    CommentCreateRequest,
    CommentListResponse,
    CommentResponse,
    CommentUpdateRequest,
)
from app.schemas.common import MAX_SQLITE_INTEGER, EntityId
from app.services.comment import CommentService

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=CommentListResponse)
async def get_comments(
    post_id: EntityId = Query(..., gt=0, le=MAX_SQLITE_INTEGER),
    skip: int = Query(0, ge=0, le=MAX_SQLITE_INTEGER),
    limit: int = Query(12, ge=1, le=100),
    service: CommentService = Depends(get_comment_service),
):
    return await service.get_comments_by_post_id(post_id, skip, limit)


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: EntityId, service: CommentService = Depends(get_comment_service)):
    return await service.get_comment_by_id_or_404(comment_id)


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    data: CommentCreateRequest,
    service: CommentService = Depends(get_comment_service),
    current_user: User = Depends(get_current_user),
):
    return await service.create_comment(data, current_user)


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: EntityId,
    data: CommentUpdateRequest,
    service: CommentService = Depends(get_comment_service),
    current_user: User = Depends(get_current_user),
):
    return await service.update_comment(comment_id, data, current_user)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: EntityId,
    service: CommentService = Depends(get_comment_service),
    current_user: User = Depends(get_current_user),
):
    await service.delete_comment(comment_id, current_user)
    return {"detail": "Comment deleted"}
