from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.category import CategoryResponse
from app.schemas.common import EntityId


class PostRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=200, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    content: str = Field(min_length=1)
    image: str | None = None
    video: str | None = None
    category_ids: list[EntityId] = Field(default_factory=list)


class Stats(BaseModel):
    post_id: int
    comments_count: int
    views: int
    model_config = ConfigDict(from_attributes=True)


class PostResponse(BaseModel):
    id: int
    name: str
    slug: str
    content: str
    description: str
    image: str | None
    main_image: str | None
    video: str | None
    user_id: int
    created_at: datetime
    updated_at: datetime
    categories: list[CategoryResponse]
    stats: Stats | None = None
    model_config = ConfigDict(from_attributes=True)


class PostListResponse(BaseModel):
    items: list[PostResponse]
    total: int
    page: int
    per_page: int
