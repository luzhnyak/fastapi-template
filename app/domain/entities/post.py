from dataclasses import dataclass
from typing import List

from app.domain.entities.base_article import BaseArticle


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
    icon: str = "icon-folder"

    @property
    def image(self):
        return f"/static/img/category/resize/{self.slug}.jpg"

    @property
    def path(self):
        return "posts/?category="


@dataclass
class Post(BaseArticle):
    id: int
    stats: PostStats
    user_id: int | None
    categories: List[Category]

    @property
    def icon(self):
        return "icon-file-alt"

    @property
    def path(self):
        return "posts"

    @property
    def path_name(self):
        return "Публікації про риболовлю"

    @property
    def maket(self):
        return "IMAGE_BOTTOM"


@dataclass
class PostList:
    items: List[Post]
    total: int
    page: int
    per_page: int
