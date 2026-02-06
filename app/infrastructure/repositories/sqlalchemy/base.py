from typing import Generic, TypeVar, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.orm import selectinload

from app.infrastructure.mappers.base import BaseMapper

Entity = TypeVar("Entity")
Model = TypeVar("Model")


class SQLAlchemyRepository(Generic[Model, Entity]):
    model: type[Model]
    mapper: BaseMapper[Model, Entity]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, entity: Entity) -> Entity:
        data = self.mapper.to_model_dict(entity)

        stmt = insert(self.model).values(**data).returning(self.model)

        res = await self.session.execute(stmt)
        model = res.scalar_one()

        return self.mapper.to_entity(model)

    async def add_one(self, data: dict) -> Entity:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        model = res.scalar_one()
        return self.mapper.to_entity(model)

    async def add_many(self, data_list: list[dict]) -> list[Entity]:
        if not data_list:
            return []
        stmt = insert(self.model).values(data_list).returning(*self.model)
        res = await self.session.execute(stmt)
        return [self.mapper.to_entity(row) for row in res.scalars().all()]

    async def edit_one(self, id: int, data: dict) -> Entity:
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model)
        res = await self.session.execute(stmt)
        model = res.scalar_one()
        return self.mapper.to_entity(model)

    async def find_one(self, **filter_by) -> Optional[Entity]:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)

        model = res.scalar_one_or_none()

        if not model:
            return None

        return self.mapper.to_entity(model)

    async def find_one_with_stats(self, **filter_by) -> Optional[Entity]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.stats))
            .filter_by(**filter_by)
        )
        res = await self.session.execute(stmt)

        model = res.scalar_one_or_none()

        if not model:
            return None

        return self.mapper.to_entity(model)

    async def find_many(
        self, skip: int = 0, limit: int = 12, **filter_by
    ) -> List[Entity]:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt.offset(skip).limit(limit))
        models = res.scalars().all()

        return [self.mapper.to_entity(m) for m in models]

    async def find_many_with_stats(
        self, skip: int = 0, limit: int = 12, **filter_by
    ) -> List[Entity]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.stats))
            .filter_by(**filter_by)
            .offset(skip)
            .limit(limit)
        )
        res = await self.session.execute(stmt)

        models = res.scalars().all()

        return [self.mapper.to_entity(m) for m in models]

    async def find_all(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        models = res.scalars().all()
        return [self.mapper.to_entity(m) for m in models]

    async def delete_one(self, id: int) -> Entity:
        stmt = (
            delete(self.model).filter_by(id=id).returning(*self.model.__table__.columns)
        )
        res = await self.session.execute(stmt)
        model = res.scalar_one()
        if model is None:
            raise ValueError("Record not found")
        return self.mapper.to_entity(model)

    async def delete(self, id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        return res.rowcount > 0

    async def count(self, **filters) -> int:
        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def count_all(self, **filter_by) -> int:
        stmt = select(func.count()).select_from(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalar_one()
