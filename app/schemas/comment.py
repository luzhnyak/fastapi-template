from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import EntityId
from app.schemas.user import RelationshipUserResponse


class CommentCreateRequest(BaseModel):
    post_id: EntityId
    content: str = Field(min_length=1, max_length=10000)


class CommentUpdateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=10000)


class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str
    created_at: datetime
    updated_at: datetime
    user: RelationshipUserResponse
    model_config = ConfigDict(from_attributes=True)


class CommentListResponse(BaseModel):
    items: list[CommentResponse]
    total: int
    page: int
    per_page: int
