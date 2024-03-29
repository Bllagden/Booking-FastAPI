from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from dao import BookingDAO
from db.models import Users
from exceptions import BookingNotExist, RoomCannotBeBooked
from tasks import send_booking_confirmation_email

from ..users.dependencies import get_current_user
from .schemas import SBookings, SNewBooking

router_bookings = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router_bookings.get("/get")
async def get_bookings(
    user: Users = Depends(get_current_user),  # noqa: B008
) -> list[SBookings]:
    return await BookingDAO.find_all(user_id=user.id)


@router_bookings.post("/add", status_code=200)
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user),  # noqa: B008
) -> SNewBooking:
    booking = await BookingDAO.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )

    if not booking:
        raise RoomCannotBeBooked

    booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    send_booking_confirmation_email.delay(booking, user.email)
    return booking


@router_bookings.delete("/{booking_id}")
async def cancel_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),  # noqa: B008
) -> dict[str, str]:
    success = await BookingDAO.delete(booking_id, user.id)

    if not success:
        raise BookingNotExist

    return {"message": "Бронь отменена"}
