from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, computed_field
from typing import List

from app.utils.strip_tags_and_trim import strip_tags_and_trim


class Stats(BaseModel):
    article_id: int
    comments_count: int
    views: int

    model_config = ConfigDict(from_attributes=True)


class BaseArticle(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    image: str | None
    thumbnail: str | None
    main_image: str | None
    created_at: datetime
    updated_at: datetime
    path: str
    stats: Stats | None = None

    model_config = ConfigDict(from_attributes=True)


class BaseArticleFull(BaseArticle):
    content: str
    video: str | None


class RelationshipResponse(BaseModel):
    id: int
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)
