from typing import Optional

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.models.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    lastvisit_date: Mapped[Optional[str]] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="user")
    avatar: Mapped[Optional[str]] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    posts: Mapped[list["PostModel"]] = relationship("PostModel", back_populates="user")  # type: ignore
    comments: Mapped[list["CommentModel"]] = relationship("CommentModel", back_populates="user")  # type: ignore
