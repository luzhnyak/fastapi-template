from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.infrastructure.models.comment import CommentModel
    from app.infrastructure.models.post import PostModel


class UserModel(BaseModel):
    __tablename__ = "users"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    lastvisit_date: Mapped[str | None] = mapped_column(String)
    google_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    role: Mapped[str] = mapped_column(String, default="user")
    avatar: Mapped[str | None] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    posts: Mapped[list[PostModel]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    comments: Mapped[list[CommentModel]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
