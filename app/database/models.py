from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

from datetime import datetime

Base = declarative_base()  # Базовый класс для моделей


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # ID пользователя
    username = Column(String(100), nullable=False)  # Имя пользователя (First name)
    tg_id = Column(Integer, unique=True, nullable=False)  # Telegram ID пользователя
    nickname = Column(String(100), unique=True, nullable=True)  # Никнейм (@username)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)  # ID поста
    user_id = Column(Integer, nullable=False)  # ID автора
    post_type = Column(String(10), nullable=False) # Пост либо приватный либо публичный
    text = Column(Text, nullable=False)  # Текст поста
    created_at = Column(DateTime, default=datetime.utcnow)  # Время создания поста (UTC)