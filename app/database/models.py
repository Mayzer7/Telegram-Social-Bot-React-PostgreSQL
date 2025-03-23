from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()  # Базовый класс для моделей

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # ID пользователя
    username = Column(String(100), nullable=False)  # Имя пользователя
    tg_id = Column(Integer, unique=True, nullable=False)  # Telegram ID пользователя

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)  # ID поста
    user_id = Column(Integer, nullable=False)  # ID автора
    text = Column(Text, nullable=False)  # Текст поста