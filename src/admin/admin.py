from sqladmin import Admin

from db import async_engine

from .views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin


def create_admin(app):
    admin = Admin(app, async_engine)
    _add_admin_views(admin)
    return admin


def _add_admin_views(admin):
    admin.add_view(UsersAdmin)
    admin.add_view(HotelsAdmin)
    admin.add_view(RoomsAdmin)
    admin.add_view(BookingsAdmin)
