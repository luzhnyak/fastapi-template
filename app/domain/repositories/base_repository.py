from abc import ABC, abstractmethod
from typing import Generic, Optional, List, TypeVar


Entity = TypeVar("Entity")


class BaseRepository(Generic[Entity], ABC):
    @abstractmethod
    async def find_one(self, **filter_by) -> Optional[Entity]:
        pass

    @abstractmethod
    async def find_one_with_stats(self, **filter_by) -> Optional[Entity]:
        pass

    @abstractmethod
    async def find_many(self, skip: int, limit: int, **filter_by) -> List[Entity]:
        pass

    @abstractmethod
    async def find_many_with_stats(
        self, skip: int, limit: int, **filter_by
    ) -> List[Entity]:
        pass

    @abstractmethod
    async def find_all(self, **filter_by):
        pass

    @abstractmethod
    async def count_all(self, **filter_by) -> int:
        pass
