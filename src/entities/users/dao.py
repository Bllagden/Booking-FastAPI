from base_dao import BaseDAO
from db.models import Users


class UsersDAO(BaseDAO):
    model = Users
