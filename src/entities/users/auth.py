from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from exceptions import IncorrectEmailOrPasswordException
from settings import auth_settings

from .dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token_expires = timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashes_password) -> bool:
    return pwd_context.verify(plain_password, hashes_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # expire = datetime.utcnow() + timedelta(minutes=30)
    expire = datetime.utcnow() + access_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, auth_settings.SECRET_KEY, auth_settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user:
        raise IncorrectEmailOrPasswordException
    if not verify_password(password, user.hashed_password):
        raise IncorrectEmailOrPasswordException
    return user
