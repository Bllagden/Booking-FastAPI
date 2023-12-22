from sqlalchemy import insert, select

from db.engine import async_session_factory


class BaseDAO:
    """if mappings() => .__table__.columns"""

    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_factory() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        """.filter(*filter_by)
        router return await:
        BookingsDAO.find_all(Bookings.total_days > 14, Bookings.price <= 9000)"""
        async with async_session_factory() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        """query = ...(**data).returning(cls.model.id)"""
        async with async_session_factory() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()