# from typing import TYPE_CHECKING

from sqlalchemy import insert, select
from sqlalchemy.engine.row import RowMapping

from db.engine import async_session_factory


class BaseDAO:
    """DAO (Data Access Objects) - объекты, предоставляющие абстрактный интерфейс для работы с БД."""

    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> RowMapping | None:
        """Возвращает полную строку или None.
        cls.model.__table__.columns  =>   {'id': 1, ...}
        cls.model                    =>   {'Candies': <db.candies_model.Candies>}"""
        async with async_session_factory() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            res = await session.execute(query)
            return res.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by) -> list[RowMapping]:
        """
        .filter(*filter_by)
            router_bookings: get_bookings
                return await
                BookingsDAO.find_all(Bookings.total_days > 14, Bookings.price <= 9000)
        """
        async with async_session_factory() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            res = await session.execute(query)
            return res.mappings().all()

    @classmethod
    async def add(cls, **data) -> None:
        """Добавленное значение возвращается методом .returning()"""
        async with async_session_factory() as session:
            stmt = insert(cls.model).values(**data)  # .returning(cls.model.id)
            new_object = await session.execute(stmt)
            await session.commit()
            # return new_object.scalar_one()
