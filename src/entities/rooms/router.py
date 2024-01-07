from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from db.models import Users
from exceptions import RoomCannotBeCreated

from ..users.dependencies import get_current_user
from .dao import RoomsDAO
from .schemas import SNewRoom, SRooms

router_rooms = APIRouter(
    prefix="/rooms",
    tags=["Комнаты"],
)


@router_rooms.get("")
async def get_hotels(user: Users = Depends(get_current_user)) -> list[SRooms]:
    return await RoomsDAO.find_all()


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
