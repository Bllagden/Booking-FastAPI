from fastapi import APIRouter, Depends

from db.models import Users

from ..users.dependencies import get_current_user
from .dao import BookingDAO
from .schemas import SBookings, SNewBooking

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("/add")
async def add_booking(user: Users = Depends(get_current_user)):
    await BookingDAO.add()
