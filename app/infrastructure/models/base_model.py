from datetime import datetime

from sqlalchemy import Boolean, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.database import Base


class BaseModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class ArticlesBaseModel(BaseModel):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String, default="Post")
    slug: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    hits: Mapped[int] = mapped_column(Integer)
    video: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)
    thumbnail: Mapped[str] = mapped_column(String)
    ena: Mapped[bool] = mapped_column(Boolean, default=False)
