from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from base_dao import BaseDAO
from db.engine import async_session_factory
from db.models import Rooms
from logger import logger


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def add(
        cls,
        hotel_id: int,
        name: str,
        description: str | None,
        price: int,
        services: list[str],
        quantity: int,
        image_id: int,
    ):
        try:
            async with async_session_factory() as session:
                add_room = (
                    insert(Rooms)
                    .values(
                        hotel_id=hotel_id,
                        name=name,
                        description=description,
                        price=price,
                        services=services,
                        quantity=quantity,
                        image_id=image_id,
                    )
                    .returning(Rooms.__table__.c)
                )

                new_room = await session.execute(add_room)
                await session.commit()
                return new_room.mappings().one()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add room"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add room"
            extra = {
                "hotel_id": hotel_id,
                "name": name,
                "description": description,
                "price": price,
                "services": services,
                "quantity": quantity,
                "image_id": image_id,
            }
            logger.error(msg, extra=extra, exc_info=True)
