from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_current_user, get_post_service
from app.domain.entities.user import User
from app.schemas.common import MAX_SQLITE_INTEGER, EntityId
from app.schemas.post import PostListResponse, PostRequest, PostResponse
from app.services.post import PostService

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    data: PostRequest,
    service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    return await service.create_post(data, current_user)


@router.get("/", response_model=PostListResponse)
async def get_posts(
    skip: int = Query(0, ge=0, le=MAX_SQLITE_INTEGER),
    limit: int = Query(12, ge=1, le=100),
    service: PostService = Depends(get_post_service),
):
    return await service.get_posts(skip, limit)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post_by_id(post_id: EntityId, service: PostService = Depends(get_post_service)):
    return await service.get_post_by_id_or_404(post_id)


@router.get("/{slug}/slug", response_model=PostResponse)
async def get_post_by_slug(slug: str, service: PostService = Depends(get_post_service)):
    return await service.get_post_by_slug_or_404(slug)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: EntityId,
    data: PostRequest,
    service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    return await service.update_post(post_id, data, current_user)


@router.delete("/{post_id}")
async def delete_post(
    post_id: EntityId,
    service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    post = await service.delete_post(post_id, current_user)
    return {"detail": f"Post {post.name} deleted"}
