from datetime import date

from pydantic import BaseModel


class SBookings(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    # Чтобы при сериализации модели Pydantic пытался прочитать атрибуты данных
    # (через точку), а не словарь ( ["key"] )
    class Config:
        from_attributes = True


class SNewBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date