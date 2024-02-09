from datetime import date

from pydantic import BaseModel, ConfigDict


class SBookings(BaseModel):
    """from_attributes=True - сериализация данных в модель Pydantic для orm объектов
    (обращение к атрибутам через точку, а не по ключам словаря)."""

    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    # новый способ
    model_config = ConfigDict(from_attributes=True)

    # старый способ
    # class Config:
    #   from_attributes = True


class SNewBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
