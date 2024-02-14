from fastapi import HTTPException, status


class BookingException(HTTPException):
    """Во время поднятия исключения (raise) создается экземпляр класса этого исключения.

    Почему self.status_code и self.detail:
    При создании экземпляра, поля класса становятся полями экземпляра класса.

    status_code является обязательным параметром в HTTPException, поэтому необходимо
    вызывать super().__init__ для передачи status_code в HTTPException."""

    status_code = 500
    detail = ""

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomFullyBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось забронировать номер ввиду неизвестной ошибки"


class HotelCannotBeCreated(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось создать отель ввиду неизвестной ошибки"


class RoomCannotBeCreated(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось создать комнату ввиду неизвестной ошибки"


class BookingNotExist(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Бронь не найдена"
