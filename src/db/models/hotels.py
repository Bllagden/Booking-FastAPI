from typing import TYPE_CHECKING

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base, int_pk

if TYPE_CHECKING:
    from db.models import Rooms


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int_pk]
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]

    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")

    def __str__(self):
        return self.name
