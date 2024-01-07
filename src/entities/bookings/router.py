from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from db.models import Users
from exceptions import RoomCannotBeBooked

from ..users.dependencies import get_current_user
from .dao import BookingDAO
from .schemas import SBookings, SNewBooking

router_bookings = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router_bookings.get("/get")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingDAO.find_all(user_id=user.id)


@router_bookings.post("", status_code=200)
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )

    if not booking:
        raise RoomCannotBeBooked

    booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    return booking
