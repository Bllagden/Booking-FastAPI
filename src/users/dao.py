from src.users.models import Users
from src.dao.base import BaseDAO


class UsersDAO(BaseDAO):
    model = Users
