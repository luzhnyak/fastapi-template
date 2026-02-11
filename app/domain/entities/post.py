from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from app.utils.strip_tags_and_trim import strip_tags_and_trim


@dataclass
class PostStats:
    article_id: int
    comments_count: int
    views: int


@dataclass
class Category:
    id: int
    slug: str
    name: str


@dataclass(kw_only=True)
class Post:
    id: int
    name: str
    slug: str
    content: str
    created_at: datetime
    updated_at: datetime
    image: Optional[str] = None
    video: Optional[str] = None
    user_id: int | None = None

    stats: PostStats
    categories: List[Category]

    @property
    def description(self) -> str:
        return strip_tags_and_trim(self.content)


@dataclass
class PostList:
    items: List[Post]
    total: int
    page: int
    per_page: int
