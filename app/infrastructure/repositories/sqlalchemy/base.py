from typing import Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.mappers.base import BaseMapper

Entity = TypeVar("Entity")
Model = TypeVar("Model")


class SQLAlchemyRepository(Generic[Model, Entity]):
    model: type[Model]
    mapper: BaseMapper[Model, Entity]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, entity: Entity) -> Entity:
        return await self.add_one(self.mapper.to_model_dict(entity))

    async def add_one(self, data: dict) -> Entity:
        model = self.model(**data)
        self.session.add(model)
        await self.session.flush()
        return await self.find_one(id=model.id)

    async def add_many(self, data_list: list[dict]) -> list[Entity]:
        return [await self.add_one(data) for data in data_list]

    async def edit_one(self, id: int, data: dict) -> Entity:
        model = await self.session.get(self.model, id)
        if model is None:
            raise ValueError("Record not found")
        for key, value in data.items():
            setattr(model, key, value)
        await self.session.flush()
        return await self.find_one(id=id)

    async def find_one(self, **filter_by) -> Entity | None:
        stmt = select(self.model).filter_by(**filter_by).execution_options(populate_existing=True)
        model = (await self.session.execute(stmt)).scalar_one_or_none()
        return self.mapper.to_entity(model) if model is not None else None

    async def find_one_with_stats(self, **filter_by) -> Entity | None:
        return await self.find_one(**filter_by)

    async def find_many(self, skip: int = 0, limit: int = 12, **filter_by) -> list[Entity]:
        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .order_by(self.model.id)
            .offset(skip)
            .limit(limit)
        )
        return [self.mapper.to_entity(model) for model in (await self.session.scalars(stmt)).all()]

    async def find_many_with_stats(
        self, skip: int = 0, limit: int = 12, **filter_by
    ) -> list[Entity]:
        return await self.find_many(skip=skip, limit=limit, **filter_by)

    async def find_all(self, **filter_by) -> list[Entity]:
        stmt = select(self.model).filter_by(**filter_by).order_by(self.model.id)
        return [self.mapper.to_entity(model) for model in (await self.session.scalars(stmt)).all()]

    async def delete_one(self, id: int) -> Entity:
        model = await self.session.get(self.model, id)
        if model is None:
            raise ValueError("Record not found")
        entity = self.mapper.to_entity(model)
        await self.session.delete(model)
        await self.session.flush()
        return entity

    async def delete(self, id: int) -> bool:
        if await self.find_one(id=id) is None:
            return False
        await self.delete_one(id)
        return True

    async def count(self, **filters) -> int:
        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        return (await self.session.execute(stmt)).scalar_one()

    async def count_all(self, **filter_by) -> int:
        return await self.count(**filter_by)
