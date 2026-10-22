from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.user import User


@dataclass
class Comment:
    id: int
    post_id: int
    content: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: User


@dataclass
class CommentList:
    items: list[Comment]
    total: int
    page: int
    per_page: int
