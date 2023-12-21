from users.models import Users
from dao.base import BaseDAO


class UsersDAO(BaseDAO):
    model = Users
