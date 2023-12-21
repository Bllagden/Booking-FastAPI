from fastapi import APIRouter, Depends

from bookings.dao import BookingDAO
from bookings.schemas import SBookings, SNewBooking
from db.models import Users
from users.dependencies import get_current_user

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("/add")
async def add_booking(user: Users = Depends(get_current_user)):
    await BookingDAO.add()
