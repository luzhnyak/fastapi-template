from abc import ABC, abstractmethod
from typing import TypeVar, Generic

Entity = TypeVar("Entity")
Model = TypeVar("Model")


class BaseMapper(ABC, Generic[Model, Entity]):
    @abstractmethod
    def to_entity(self, model: Model) -> Entity:
        raise NotImplementedError

    @abstractmethod
    def to_model_dict(self, entity: Entity) -> dict:
        """
        Перетворює Entity → dict для insert / update
        """
        raise NotImplementedError
