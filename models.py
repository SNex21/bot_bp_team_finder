from db import Base
from sqlalchemy import Column, String, Integer
from db import engine


class User(Base): # Модель пользователя
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telid = Column(String(100), unique=True, index=True)
    username = Column(String(100), default = None)
    name = Column(String(100), default = None)
    sphere = Column(String(100), default = None)
    ed_name = Column(String(100), default = None)
    event_descr = Column(String(5000), default = None)
    hashes = Column(String(100), default = None)
    name_img = Column(String(100), default = None)
    choose = Column(String(1000), default = None)


class Check(Base):# Модель уже просмотренных пользователей
    __tablename__ = "check"

    id = Column(Integer, primary_key=True, index=True)
    telid = Column(String(100), default = None)
    us_telid = Column(String(100), default = None)


Base.metadata.create_all(engine)# Обновление моделей БД
