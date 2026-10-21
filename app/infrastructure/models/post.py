from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text, func, select
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from app.infrastructure.db.base import Base
from app.infrastructure.models.base_model import BaseModel
from app.infrastructure.models.comment import CommentModel

if TYPE_CHECKING:
    from app.infrastructure.models.user import UserModel

category_post = Table(
    "category_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True
    ),
)


class CategoryModel(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(200), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    posts: Mapped[list[PostModel]] = relationship(
        secondary=category_post, back_populates="categories"
    )


class PostStatsModel(Base):
    __tablename__ = "post_stats"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), unique=True)
    # Derive the count instead of maintaining a counter that drifts on cascades.
    comments_count: Mapped[int] = column_property(
        select(func.count(CommentModel.id))
        .where(CommentModel.post_id == post_id)
        .correlate_except(CommentModel)
        .scalar_subquery()
    )
    views: Mapped[int] = mapped_column(default=0)
    post: Mapped[PostModel] = relationship(back_populates="stats")


class PostModel(BaseModel):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(200), unique=True)
    content: Mapped[str] = mapped_column(Text)
    video: Mapped[str | None] = mapped_column(String)
    image: Mapped[str | None] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    stats: Mapped[PostStatsModel | None] = relationship(
        back_populates="post", uselist=False, lazy="selectin", cascade="all, delete-orphan"
    )
    categories: Mapped[list[CategoryModel]] = relationship(
        secondary=category_post, lazy="selectin", back_populates="posts"
    )
    user: Mapped[UserModel] = relationship(back_populates="posts")
    comments: Mapped[list[CommentModel]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )
