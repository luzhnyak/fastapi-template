from typing import Optional

from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.models.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    lastvisit_date: Mapped[Optional[str]] = mapped_column(String)
    register_date: Mapped[Optional[str]] = mapped_column(String)
    fb_id: Mapped[Optional[str]] = mapped_column(String)
    tg_id: Mapped[Optional[int]] = mapped_column(Integer)
    tg_username: Mapped[Optional[str]] = mapped_column(String)
    google_id: Mapped[Optional[str]] = mapped_column(String)
    role_id: Mapped[int] = mapped_column(Integer, default=3)
    image: Mapped[Optional[str]] = mapped_column(String)
    ip: Mapped[Optional[str]] = mapped_column(String)
    ban: Mapped[bool] = mapped_column(Boolean, default=False)
    token: Mapped[Optional[str]] = mapped_column(String)
