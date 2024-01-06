from sqladmin import ModelView

from db.models import Bookings, Hotels, Rooms, Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.bookings]  # column_list = "__all__"
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    can_edit = False
    name_plural = "Users"
    name = "User"
    icon = "fa-solid fa-user"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name_plural = "Hotels"
    name = "Hotel"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.bookings]
    name_plural = "Rooms"
    name = "Room"
    icon = "fa-solid fa-bed"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [
        Bookings.user,
        Bookings.room,
    ]
    name_plural = "Bookings"
    name = "Booking"
    icon = "fa-solid fa-book"
