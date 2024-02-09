from db.models import Users

from .base_dao import BaseDAO


class UsersDAO(BaseDAO):
    model = Users
