from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from db import Base, int_pk, str_255

if TYPE_CHECKING:
    from db.models import Bookings


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str]
    hashed_password: Mapped[str_255]

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self) -> str:
        return self.email
