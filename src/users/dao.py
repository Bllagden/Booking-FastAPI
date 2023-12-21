from dao.base import BaseDAO
from users.models import Users


class UsersDAO(BaseDAO):
    model = Users
