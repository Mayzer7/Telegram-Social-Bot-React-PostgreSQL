from sqlalchemy.future import select
from database.models import User, Post
from database.db import async_session_maker

# async def add_user(tg_id: int, username: str):
#     async with async_session_maker() as session:
#         user = User(tg_id=tg_id, username=username)
#         session.add(user)
#         await session.commit()

# async def get_user(tg_id: int):
#     async with async_session_maker() as session:
#         query = select(User).where(User.tg_id == tg_id)
#         result = await session.execute(query)
#         return result.scalars().first()

# async def add_post(user_id: int, text: str):
#     async with async_session_maker() as session:
#         post = Post(user_id=user_id, text=text)
#         session.add(post)
#         await session.commit()
