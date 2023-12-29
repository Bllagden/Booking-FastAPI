from fastapi import APIRouter, Depends, Response

from db.models import Users
from exceptions import UserAlreadyExistsException

from .auth import authenticate_user, create_access_token, get_password_hash
from .dao import UsersDAO
from .dependencies import get_current_user
from .schemas import SUserAuth, SUserMe

router_users = APIRouter(prefix="/auth", tags=["Auth & Пользователи"])

"""
1) Depends - функция для объявления зависимостей в FastAPI.
Зависимость - любая функция, которая будет выполнена перед выполнением основной.
Зависимости можно поместить в декоратор пути:
    @app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
    async def read_items():

2) Request - доступ к входящему HTTP-запросу.
Содержит информацию о запросе: заголовки, параметры запроса, тело запроса и тд.

3) Response - доступ к исходящему HTTP-ответу.
Можно использовать для управления данными ответа: статус кода, заголовки и тело ответа.
"""


@router_users.post("/register")
async def register_user(user_data: SUserAuth):
    """Создается новый user, если такого еще нет."""
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router_users.post("/login")
async def login_user(responce: Response, user_data: SUserAuth):
    """Если логин/пароль верны, то с помощью HTTP-ответа создается кука с JWT-токеном."""
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    responce.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router_users.post("/logout")
async def logout_user(responce: Response):
    """С помощью HTTP-ответа удаляется кука с JWT-токеном."""
    responce.delete_cookie("booking_access_token")


@router_users.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    """Возвращает id и email аутентифицированного пользователя, либо Exception."""
    return SUserMe(id=current_user.id, email=current_user.email)
