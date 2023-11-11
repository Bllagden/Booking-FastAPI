from fastapi import APIRouter, Depends

from src.bookings.dao import BookingDAO
from src.bookings.schemas import SBookings, SNewBooking
from src.users.dependencies import get_current_user
from src.users.models import Users

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("/add")
async def add_booking(user: Users = Depends(get_current_user)):
    await BookingDAO.add()
