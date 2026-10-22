from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Entity = TypeVar("Entity")


class BaseRepository(ABC, Generic[Entity]):
    @abstractmethod
    async def add_one(self, data: dict) -> Entity:
        pass

    @abstractmethod
    async def edit_one(self, id: int, data: dict) -> Entity:
        pass

    @abstractmethod
    async def delete_one(self, id: int) -> Entity:
        pass

    @abstractmethod
    async def find_one(self, **filter_by) -> Entity | None:
        pass

    @abstractmethod
    async def find_one_with_stats(self, **filter_by) -> Entity | None:
        pass

    @abstractmethod
    async def find_many(self, skip: int, limit: int, **filter_by) -> list[Entity]:
        pass

    @abstractmethod
    async def find_many_with_stats(self, skip: int, limit: int, **filter_by) -> list[Entity]:
        pass

    @abstractmethod
    async def find_all(self, **filter_by):
        pass

    @abstractmethod
    async def count_all(self, **filter_by) -> int:
        pass
