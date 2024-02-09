from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from db.engine import async_session_factory
from db.models import Hotels
from logger import logger

from .base_dao import BaseDAO


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def add(
        cls,
        name: str,
        location: str,
        services: list[str],
        rooms_quantity: int,
        image_id: int,
    ):
        try:
            async with async_session_factory() as session:
                add_hotel = (
                    insert(Hotels)
                    .values(
                        name=name,
                        location=location,
                        services=services,
                        rooms_quantity=rooms_quantity,
                        image_id=image_id,
                    )
                    .returning(Hotels.__table__.c)
                )

                new_hotel = await session.execute(add_hotel)
                await session.commit()
                return new_hotel.mappings().one()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add hotel"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add hotel"
            extra = {
                "name": name,
                "location": location,
                "services": services,
                "rooms_quantity": rooms_quantity,
                "image_id": image_id,
            }
            logger.error(msg, extra=extra, exc_info=True)
