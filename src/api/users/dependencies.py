from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import RowMapping

from dao import UsersDAO
from exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from settings import AuthSettings, get_settings

_auth_settings = get_settings(AuthSettings)


def _get_token(request: Request) -> str:
    """С помощью HTTP-запроса запрашивается кука с JWT-токеном."""
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(_get_token)) -> RowMapping:
    """Получает JWT-токен. Декодирует токен в полезную нагрузку (dict) и проверяет ее.
    Далее, если в ней есть subject (id), ищет его в БД. Если такой есть, возвращает юзера.
    """
    try:
        payload = jwt.decode(token, _auth_settings.secret_key, _auth_settings.algorithm)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
