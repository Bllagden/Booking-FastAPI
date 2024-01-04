from sqladmin import ModelView

from db.models import Bookings, Hotels, Rooms, Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    can_edit = False
    name_plural = "Users"
    name = "User"
    icon = "fa-solid fa-user"


class HotelsAdmin(ModelView, model=Hotels):
    # column_list = []
    name_plural = "Hotels"
    name = "Hotel"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    # column_list = []
    name_plural = "Rooms"
    name = "Room"
    icon = "fa-solid fa-bed"


class BookingsAdmin(ModelView, model=Bookings):
    # column_list = []
    name_plural = "Bookings"
    name = "Booking"
    icon = "fa-solid fa-book"
