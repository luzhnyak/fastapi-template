from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text

from app.infrastructure.models.base_model import BaseModel


class CommentModel(BaseModel):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    article_id: Mapped[int] = mapped_column(Integer)
    add_date: Mapped[str] = mapped_column(String)
    comment: Mapped[str] = mapped_column(Text)
    table_name: Mapped[str] = mapped_column(String)
    article_name: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["UserModel"] = relationship("UserModel")  # type: ignore
