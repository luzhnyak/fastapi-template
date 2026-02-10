
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey

from app.infrastructure.db.base import Base
from app.infrastructure.models.base_model import BaseModel


# Асоціативна таблиця для зв'язку "багато до багатьох"
category_post = Table(
    "category_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("category_id", Integer, ForeignKey("category.id")),
)


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)

    posts: Mapped[list["PostModel"]] = relationship(
        "PostModel", secondary=category_post, back_populates="categories"
    )


class PostStatsModel(Base):
    __tablename__ = "post_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"), unique=True, nullable=False
    )
    comments_count: Mapped[int] = mapped_column(default=0)
    views: Mapped[int] = mapped_column(default=0)

    post: Mapped["PostModel"] = relationship("PostModel", back_populates="stats")


class PostModel(BaseModel):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String, default="Post")
    slug: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    video: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    stats: Mapped["PostStatsModel"] = relationship(
        "PostStatsModel", back_populates="post", uselist=False, cascade="all, delete"
    )

    categories: Mapped[list["CategoryModel"]] = relationship(
        "CategoryModel",
        secondary=category_post,
        lazy="selectin",  # краще ніж "dynamic" у 2.0
        back_populates="posts",
    )
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="posts")  # type: ignore
    comments: Mapped[list["CommentModel"]] = relationship("CommentModel", back_populates="post")  # type: ignore
