from dataclasses import dataclass
from datetime import date

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/hotels/{hotel_id}")
def get_hotel(
    hotel_id: int,  # ---------------------параметры пути (hotel_id)
    date_from,  # -------------------------параметры
    date_to,  # ---------------------------запроса
):
    return hotel_id


# =====================================================================================
# =====================================================================================
class SHotel(BaseModel):  # pydantic
    address: str
    name: str
    stars: int = Field(ge=1, le=5)  # pydantic


@app.get("/hotels_1", response_model=list[SHotel])
def get_hotels_1(
    location: str,
    date_from: date,
    date_to: date,
    has_spa: bool = Query(None),  # has_spa: bool | None = None    (bug Pydantic 2)
    stars: int = Query(None, ge=1, le=5),
):
    hotels = [
        {"address": "123", "name": "Da", "stars": 5},
        {"address": "456", "name": "Net", "stars": 1},
    ]
    return hotels


# =====================================================================================
# =====================================================================================
@dataclass
class HotelSearchArgs:
    location: str
    date_from: date
    date_to: date
    has_spa: bool = Query(None)
    stars: int = Query(None, ge=1, le=5)


@app.get("/hotels_2")
def get_hotels_2(search_args: HotelSearchArgs = Depends()):  # fastapi
    return search_args


# =====================================================================================
# =====================================================================================
class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
def add_booking(booking: SBooking):
    pass
