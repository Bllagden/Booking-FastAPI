from datetime import date

from sqlalchemy import RowMapping, and_, delete, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from db.engine import async_session_factory
from db.models import Bookings, Rooms
from exceptions import RoomFullyBooked
from logger import logger

from .base_dao import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ) -> (RowMapping | None):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        try:
            async with async_session_factory() as session:
                existing_booking = select(Bookings).where(
                    and_(
                        Bookings.room_id == room_id,
                        Bookings.user_id == user_id,
                        date_from <= Bookings.date_to,
                    ),
                )
                result = await session.execute(existing_booking)
                existing_booking: Bookings | None = result.scalar_one_or_none()
                if existing_booking is not None:
                    raise RoomFullyBooked

                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to > date_from,
                                ),
                            ),
                        ),
                    )
                    .cte("booked_rooms")
                )

                """
                SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
                LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
                WHERE rooms.id = 1
                GROUP BY rooms.quantity, booked_rooms.room_id
                """

                get_rooms_left = (
                    select(
                        (
                            Rooms.quantity
                            - func.count(booked_rooms.c.room_id).filter(
                                booked_rooms.c.room_id.is_not(None),
                            )
                        ).label("rooms_left"),
                    )
                    .select_from(Rooms)
                    .join(
                        booked_rooms,
                        booked_rooms.c.room_id == Rooms.id,
                        isouter=True,
                    )
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )
                # logger.debug(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
                rooms_left = await session.execute(get_rooms_left)
                rooms_left: int = rooms_left.scalar()

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(
                            Bookings.id,
                            Bookings.user_id,
                            Bookings.room_id,
                            Bookings.date_from,
                            Bookings.date_to,
                        )
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.mappings().one()
                else:
                    raise RoomFullyBooked
        except RoomFullyBooked:
            raise RoomFullyBooked
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add booking"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg, extra=extra, exc_info=True)

    @classmethod
    async def delete(cls, booking_id: int, user_id: int) -> (bool | None):
        try:
            async with async_session_factory() as session:
                delete_booking = (
                    delete(Bookings)
                    .where(Bookings.id == booking_id)
                    .where(Bookings.user_id == user_id)
                )

                result = await session.execute(delete_booking)
                await session.commit()
                return result.rowcount > 0
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot delete booking"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot delete booking"
            extra = {
                "booking_id": booking_id,
                "user_id": user_id,
            }
            logger.error(msg, extra=extra, exc_info=True)
