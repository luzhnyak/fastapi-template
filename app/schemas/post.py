from pydantic import BaseModel, ConfigDict
from typing import List

from app.domain.entities.post import PostStats
from app.schemas.base_article import BaseArticle, BaseArticleFull


class PostRequest(BaseArticle):
    pass


class PostResponse(BaseArticleFull):
    id: int
    user_id: int
    stats: PostStats
    path: str = "posts"
    main_image: str | None
    description: str

    model_config = ConfigDict(from_attributes=True)


class PostListResponse(BaseModel):
    items: List[PostResponse]
    total: int
    page: int
    per_page: int
