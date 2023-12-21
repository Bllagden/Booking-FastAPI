from dao.base import BaseDAO
from db.models import Users


class UsersDAO(BaseDAO):
    model = Users
