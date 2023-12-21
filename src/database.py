from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings import db_settings

# Движок - высокоуровневый API SQLAlchemy (скрывает детали реализации) для работы с БД.
# Работа происходит через драйвер БД (например, asyncpg).
engine = create_async_engine(db_settings.url)


# Создание фабрики сессий SQLAlchemy
#   Сессия - это временная область, в которой происходит вся работа с БД.
#   Через сессию проходят все запросы, изменения данных и транзакции.
#
# Фабрика сессий - это механизм, который создает новые объекты сессии.
# async_sessionmaker возвращает связанный с параметрами экземпляр (класс AsyncSessionMaker).
# AsyncSessionMaker возвращает экземпляр класса AsyncSession.
AsyncSessionMaker = async_sessionmaker(engine, expire_on_commit=False)


# Все модели наследуются от Base => данные о моделях будут аккумулироваться в Base
# Для сравнения текущего состояния моделей с таблицами в БД (alembic)
class Base(DeclarativeBase):
    pass
