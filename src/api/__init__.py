from .bookings.router import router_bookings
from .hotels.router import router_hotels
from .rooms.router import router_rooms
from .users.router import router_users

__all__ = [
    "router_bookings",
    "router_hotels",
    "router_rooms",
    "router_users",
]
