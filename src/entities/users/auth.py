from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.engine.row import RowMapping

from exceptions import IncorrectEmailOrPasswordException
from settings import auth_settings

from .dao import UsersDAO

# Контекст для хеширования паролей с использованием алгоритма bcrypt
# Класс CryptContext имеет методы hash, verify и тд. для работы с паролями
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Получает пароль, делает из него хеш и возвращает его."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashes_password: str) -> bool:
    """Получает пароль и хеш ?этого? пароля из БД, возвращает bool их сравнения."""
    return pwd_context.verify(plain_password, hashes_password)


def create_access_token(data: dict) -> str:
    """Создание JWT-токена. Истекает через 'access_token_expires'."""
    access_token_expires = timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # timedelta - разница между двумя объектами datetime (можно прибавить к datetime объекту)

    to_encode = data.copy()  # {'sub': '1'}     # '1' - id
    expire = datetime.utcnow() + access_token_expires
    to_encode.update({"exp": expire})  # {'sub': '1', 'exp': datetime(2023, 12, ...)}

    encoded_jwt = jwt.encode(
        to_encode, auth_settings.SECRET_KEY, auth_settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str) -> RowMapping:
    """Если логин/пароль верны, возвращает пользователя."""
    user: RowMapping | None = await UsersDAO.find_one_or_none(email=email)
    if not user:
        raise IncorrectEmailOrPasswordException
    if not verify_password(password, user.hashed_password):
        raise IncorrectEmailOrPasswordException
    return user
