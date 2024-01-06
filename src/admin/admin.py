from sqladmin import Admin

from db import async_session_factory

from .views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin


def create_admin(app):
    admin = Admin(app, session_maker=async_session_factory)
    _add_admin_views(admin)
    return admin


def _add_admin_views(admin):
    admin.add_view(UsersAdmin)
    admin.add_view(HotelsAdmin)
    admin.add_view(RoomsAdmin)
    admin.add_view(BookingsAdmin)
