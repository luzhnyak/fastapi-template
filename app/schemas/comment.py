from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List

from app.schemas.user import RelationshipUserResponse, UserResponse


class CommentCreateRequest(BaseModel):
    post_id: int
    content: str


class CommentUpdateRequest(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str
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
