from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List

from app.schemas.user import RelationshipUserResponse, UserResponse


class CommentCreateRequest(BaseModel):
    article_id: int
    created_at: str
    comment: str
    table_name: str
    user_id: int


class CommentUpdateRequest(BaseModel):
    article_id: int
    created_at: str
    comment: str
    table_name: str
    user_id: int


class CommentResponse(BaseModel):
    id: int
    article_id: int
    user_id: int
    text: str
    table_name: str
    created_at: datetime
    updated_at: datetime
    user: RelationshipUserResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class CommentListResponse(BaseModel):
    items: List[CommentResponse]
    total: int
    page: int
    per_page: int

    model_config = ConfigDict(from_attributes=True)
