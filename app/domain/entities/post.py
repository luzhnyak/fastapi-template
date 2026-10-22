from dataclasses import dataclass, field
from datetime import datetime

from app.utils.strip_tags_and_trim import strip_tags_and_trim


@dataclass
class PostStats:
    post_id: int
    comments_count: int
    views: int


@dataclass
class Category:
    id: int
    slug: str
    name: str


@dataclass
class CategoryList:
    items: list[Category]
    total: int
    page: int
    per_page: int


@dataclass(kw_only=True)
class Post:
    id: int
    name: str
    slug: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    image: str | None = None
    video: str | None = None
    stats: PostStats | None = None
    categories: list[Category] = field(default_factory=list)

    @property
    def description(self) -> str:
        return strip_tags_and_trim(self.content)

    @property
    def main_image(self) -> str | None:
        return self.image


@dataclass
class PostList:
    items: list[Post]
    total: int
    page: int
    per_page: int
