from typing import Generic, List, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int

    model_config = ConfigDict(from_attributes=True)
