from sqladmin import Admin

from db import async_engine, async_session_factory  # noqa: F401

from .auth import authentication_backend
from .views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin


def create_admin(app):
    admin = Admin(
        app,
        # engine=async_engine,
        session_maker=async_session_factory,
        authentication_backend=authentication_backend,
    )
    _add_admin_views(admin)
    return admin


def _add_admin_views(admin):
    admin.add_view(UsersAdmin)
    admin.add_view(HotelsAdmin)
    admin.add_view(RoomsAdmin)
    admin.add_view(BookingsAdmin)
