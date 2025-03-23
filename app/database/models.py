from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger
from datetime import datetime

Base = declarative_base()  # Базовый класс для моделей

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)  # ID пользователя (BigInteger)
    username = Column(String(100), nullable=False)  # Имя пользователя (First name)
    tg_id = Column(BigInteger, unique=True, nullable=False)  # Telegram ID пользователя (BigInteger)
    nickname = Column(String(100), unique=True, nullable=True)  # Никнейм (@username)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)  # ID поста
    user_id = Column(BigInteger, nullable=False)  # ID автора (BigInteger)
    post_type = Column(String(10), nullable=False)  # Тип поста (приватный или публичный)
    text = Column(Text, nullable=False)  # Текст поста
    created_at = Column(DateTime, default=datetime.utcnow)  # Время создания поста (UTC)