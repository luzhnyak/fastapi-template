from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Text

from app.infrastructure.models.base_model import BaseModel


class CommentModel(BaseModel):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    content: Mapped[str] = mapped_column(Text)
    post_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["UserModel"] = relationship("UserModel")  # type: ignore
    post: Mapped["PostModel"] = relationship("PostModel")  # type: ignore
