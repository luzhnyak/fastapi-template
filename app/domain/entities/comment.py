from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.domain.entities.user import User, UserMinimal


@dataclass
class Comment:
    id: int
    article_id: int
    comment: str
    table_name: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: UserMinimal | None = None

    @property
    def text(self) -> str:
        return self.comment


@dataclass
class CommentList:
    items: List[Comment]
    total: int
    page: int
    per_page: int
