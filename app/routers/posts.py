from fastapi import APIRouter, Depends, status


from app.api.dependencies import get_current_user, get_post_service
from app.schemas.post import PostListResponse, PostRequest, PostResponse
from app.schemas.user import UserResponse
from app.services.post import PostService


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    data: PostRequest,
    service: PostService = Depends(get_post_service),
    current_user: UserResponse = Depends(get_current_user),
):
    post = await service.create_post(data, current_user.id)
    return post


@router.get("/", response_model=PostListResponse)
async def get_posts(
    skip: int = 0, limit: int = 12, service: PostService = Depends(get_post_service)
):
    return await service.get_posts(skip, limit)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post_by_id(
    post_id: int, service: PostService = Depends(get_post_service)
):
    post = await service.get_post_by_id(post_id)
    return post


@router.get("/{slug}/slug", response_model=PostResponse)
async def get_post_by_slug(slug: str, service: PostService = Depends(get_post_service)):
    post = await service.get_post_by_slug_or_404(slug)
    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    id: int,
    data: PostRequest,
    service: PostService = Depends(get_post_service),
    current_user: UserResponse = Depends(get_current_user),
):
    updated_post = await service.update_post(id, data, current_user.id)

    return updated_post


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    service: PostService = Depends(get_post_service),
    current_user: UserResponse = Depends(get_current_user),
):
    deleted_post = await service.delete_post(post_id, current_user.id)
    return {"detail": f"Post {deleted_post.name} deleted"}
