from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime


class PostRequest(BaseModel):
    name: str
    slug: str
    content: str
    image: str | None = None
    video: str | None = None
    category_ids: List[int]

    model_config = ConfigDict(from_attributes=True)


class Stats(BaseModel):
    article_id: int
    comments_count: int
    views: int

    model_config = ConfigDict(from_attributes=True)


class RelationshipResponse(BaseModel):
    id: int
    name: str
    slug: str

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
    stats: Stats | None = None

    model_config = ConfigDict(from_attributes=True)


class PostListResponse(BaseModel):
    items: List[PostResponse]
    total: int
    page: int
    per_page: int
