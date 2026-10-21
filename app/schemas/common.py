from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    per_page: int

    model_config = ConfigDict(from_attributes=True)


MAX_SQLITE_INTEGER = 2**63 - 1
EntityId = Annotated[int, Field(ge=1, le=MAX_SQLITE_INTEGER)]
