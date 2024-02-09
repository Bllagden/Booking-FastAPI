import asyncio

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from pydantic import TypeAdapter

from dao import RoomsDAO
from db.models import Users
from exceptions import RoomCannotBeCreated

from ..users.dependencies import get_current_user
from .schemas import SNewRoom, SRooms

router_rooms = APIRouter(
    prefix="/rooms",
    tags=["Комнаты"],
)


@router_rooms.get("/hotel_id/{hotel_id}")
@cache(expire=30)
async def get_rooms_by_hotel_id(hotel_id: int) -> list[SRooms]:
    await asyncio.sleep(3)
    return await RoomsDAO.find_all(hotel_id=hotel_id)


@router_rooms.post("/add")
async def add_room(
    room: SNewRoom,
    user: Users = Depends(get_current_user),
):
    room = await RoomsDAO.add(
        room.hotel_id,
        room.name,
        room.description,
        room.price,
        room.services,
        room.quantity,
        room.image_id,
    )

    if not room:
        raise RoomCannotBeCreated

    room = TypeAdapter(SNewRoom).validate_python(room).model_dump()
    return room
