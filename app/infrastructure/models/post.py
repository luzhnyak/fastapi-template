from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey

from app.infrastructure.db.database import Base
from app.infrastructure.models.base_model import ArticlesBaseModel
from app.infrastructure.models.base_model import BaseModel


# Асоціативна таблиця для зв'язку "багато до багатьох"
category_post = Table(
    "category_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("category_id", Integer, ForeignKey("category.id")),
)


class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    maket: Mapped[str] = mapped_column(String)

    posts: Mapped[list["PostModel"]] = relationship(
        "PostModel", secondary=category_post, back_populates="categories"
    )


class PostStatsModel(Base):
    __tablename__ = "post_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"), unique=True, nullable=False
    )
    comments_count: Mapped[int] = mapped_column(default=0)
    views: Mapped[int] = mapped_column(default=0)

    post: Mapped["PostModel"] = relationship("PostModel", back_populates="stats")


class PostModel(ArticlesBaseModel):
    __tablename__ = "posts"

    is_gallery: Mapped[str] = mapped_column(String)
    maket: Mapped[str] = mapped_column(String)
    ena: Mapped[str] = mapped_column(String)
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
