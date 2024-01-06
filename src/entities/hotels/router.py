from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from db.models import Users
from exceptions import RoomCannotBeBooked

from ..users.dependencies import get_current_user
from .dao import HotelsDAO
from .schemas import SHotels, SNewHotel

router_hotels = APIRouter(prefix="/hotels", tags=["Отели"])


@router_hotels.get("")
async def get_hotels(user: Users = Depends(get_current_user)) -> list[SHotels]:
    return await HotelsDAO.find_all()


@router_hotels.post("/add")
async def add_hotel(
    hotel: SNewHotel,
    user: Users = Depends(get_current_user),
):
    hotel = await HotelsDAO.add(
        hotel.name,
        hotel.location,
        hotel.services,
        hotel.rooms_quantity,
        hotel.image_id,
    )

    if not hotel:
        raise RoomCannotBeBooked

    hotel = TypeAdapter(SNewHotel).validate_python(hotel).model_dump()
    return hotel
