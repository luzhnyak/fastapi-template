from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.infrastructure.models.post import PostModel
    from app.infrastructure.models.user import UserModel


class CommentModel(BaseModel):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    user: Mapped[UserModel] = relationship(back_populates="comments", lazy="selectin")
    post: Mapped[PostModel] = relationship(back_populates="comments")
