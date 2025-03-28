import os
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards import global_reply_keyboard, my_comands_text, my_comands, post_categories, cancel, type_posts, methods_view_posts
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext 
from states import WritePost

from sqlalchemy.future import select
from database.db import async_session_maker
from database.models import Post, User

from datetime import datetime, timedelta

router = Router()

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY") 

async def upload_to_imgbb(image_bytes):
    """Загружает изображение на imgbb и возвращает ссылку."""
    url = "https://api.imgbb.com/1/upload"
    params = {"key": IMGBB_API_KEY}
    
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field("image", image_bytes)
        
        async with session.post(url, data=form, params=params) as response:
            data = await response.json()
            return data.get("data", {}).get("url")
        
        
async def get_user_avatar(bot, user_id):
    """Получает аватар пользователя, загружает на imgbb и возвращает ссылку."""
    photos = await bot.get_user_profile_photos(user_id, limit=1)
    
    if photos.photos:
        file_id = photos.photos[0][-1].file_id  # Берем самое большое фото
        file = await bot.get_file(file_id)
        file_path = file.file_path
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.telegram.org/file/bot{bot.token}/{file_path}") as resp:
                image_bytes = await resp.read()
                return await upload_to_imgbb(image_bytes)

    return None  # Если фото нет

@router.message(F.text == '/start')
async def hello(message: Message, state: FSMContext, bot):
    async with async_session_maker() as session:
        existing_user = await session.execute(select(User).filter_by(tg_id=message.from_user.id))
        existing_user = existing_user.scalar_one_or_none()

        if not existing_user:
            avatar_url = await get_user_avatar(bot, message.from_user.id)
            
            new_user = User(
                tg_id=message.from_user.id,
                username=message.from_user.first_name,
                nickname=message.from_user.username,
                image_url=avatar_url  # Сохраняем ссылку в БД
            )
            session.add(new_user)
            await session.commit()
    
    current_state = await state.get_state()
    if current_state == WritePost.waiting_for_text.state:
        data = await state.get_data()
        post_type = data.get("post_type", "public")
        post_type_text = "публичный" if post_type == "public" else "приватный"
        await message.answer(
            f"Вы начали писать {post_type_text} пост. Напишите его, чтобы я мог сохранить или нажмите отмена", 
            reply_markup=cancel
        )
    else:
        await message.answer('Привет, я бот для заметок', reply_markup=global_reply_keyboard)
    
@router.message(F.text == 'Главное меню')
async def show_commands(message: Message):
    await message.answer("Вот мои команды:", reply_markup=my_comands)

@router.callback_query(F.data == 'add_post')
async def show_add_post(callback: CallbackQuery):
    await callback.message.edit_text("Выберите категорию поста", reply_markup=post_categories)

@router.callback_query(F.data == 'choose_method_view_posts')
async def choose_method_view_posts(callback: CallbackQuery):
    await callback.message.edit_text("Выберите способ отображения постов", reply_markup=methods_view_posts)

# Показать все посты пользователей
@router.callback_query(F.data == 'in_telegram')
async def in_telegram(callback: CallbackQuery):
    await callback.message.edit_text("Вы выбрали показать все посты в самом тг")
    
    # Подключаемся к базе данных
    async with async_session_maker() as session:
        # Получаем все посты из базы данных
        result = await session.execute(select(Post).filter_by(post_type="public"))
        posts = result.scalars().all()
        
        # Если посты найдены, выводим их
        if posts:
            for post in posts:
                # Получаем пользователя, который создал данный пост
                post_user_result = await session.execute(select(User).where(User.tg_id == post.user_id))  # Используем where вместо filter_by
                post_user = post_user_result.scalars().first()
                
                # Получаем никнейм постящего пользователя
                post_user_nickname = post_user.nickname if post_user and post_user.nickname else "Никнейм не установлен"
                
                post_text = f"Ник: @{post_user_nickname}\nТип поста: {post.post_type}\nТекст: {post.text}\nДата создания: {post.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                await callback.message.answer(post_text)
        else:
            await callback.message.answer("Постов нет.")

    
# Показать только мои посты
@router.callback_query(F.data == 'show_my_posts')
async def show_my_posts(callback: CallbackQuery):
    await callback.message.edit_text("Выберите тип постов", reply_markup=type_posts)
    



@router.callback_query(F.data == "type_public_posts")
async def show_public_posts(callback: CallbackQuery):
    await callback.answer()
    # Получаем tg_user_id из callback'а
    tg_user_id = callback.from_user.id
    
    # Подключаемся к базе данных
    async with async_session_maker() as session:
        # Получаем пользователя по tg_id
        result = await session.execute(select(User).filter_by(tg_id=tg_user_id))
        user = result.scalars().first()

        # Если пользователь найден
        if user:
            # Получаем nickname
            nickname = user.nickname if user.nickname else "Никнейм не установлен"
            
            # Получаем все посты пользователя
            result = await session.execute(select(Post).filter_by(user_id=tg_user_id, post_type="public"))
            posts = result.scalars().all()
            
            # Если посты найдены, выводим их
            if posts:
                for post in posts:
                    post_text = f"Ник: @{nickname}\nТип поста: {post.post_type}\nТекст: {post.text}\nДата создания: {post.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                    await callback.message.answer(post_text)
            else:
                await callback.message.answer("У вас нет постов.")
        
        else:
            await callback.message.answer("Пользователь не найден.")
            
            

@router.callback_query(F.data == "type_private_posts")
async def show_private_posts(callback: CallbackQuery):
    await callback.answer()
    # Получаем tg_user_id из callback'а
    tg_user_id = callback.from_user.id
    
    # Подключаемся к базе данных
    async with async_session_maker() as session:
        # Получаем пользователя по tg_id
        result = await session.execute(select(User).filter_by(tg_id=tg_user_id))
        user = result.scalars().first()

        # Если пользователь найден
        if user:
            # Получаем nickname
            nickname = user.nickname if user.nickname else "Никнейм не установлен"
            
            # Получаем все посты пользователя
            result = await session.execute(select(Post).filter_by(user_id=tg_user_id, post_type="private"))
            posts = result.scalars().all()
            
            # Если посты найдены, выводим их
            if posts:
                for post in posts:
                    post_text = f"Ник: @{nickname}\nТип поста: {post.post_type}\nТекст: {post.text}\nДата создания: {post.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                    await callback.message.answer(post_text)
            else:
                await callback.message.answer("У вас нет постов.")
        
        else:
            await callback.message.answer("Пользователь не найден.")
    
    


    
    
    
# Обработчик для публичного поста
@router.callback_query(F.data == 'public_post')
async def show_add_post(callback: CallbackQuery, state: FSMContext):
    await state.update_data(post_type="public")  # Запоминаем тип поста
    await callback.message.edit_text("Напишите публичный пост", reply_markup=cancel)
    await state.set_state(WritePost.waiting_for_text)

# Обработчик для приватного поста
@router.callback_query(F.data == 'private_post')
async def show_add_private_post(callback: CallbackQuery, state: FSMContext):
    await state.update_data(post_type="private")  # Запоминаем тип поста
    await callback.message.edit_text("Напишите приватный пост:", reply_markup=cancel)
    await state.set_state(WritePost.waiting_for_text)

# Универсальный обработчик для сохранения постов
@router.message(WritePost.waiting_for_text)
async def receive_post_text(message: Message, state: FSMContext):
    data = await state.get_data()
    post_type = data.get("post_type", "public")  # Получаем тип поста
    post_text = message.text  
    user_id = message.from_user.id  

    async with async_session_maker() as session:
        async with session.begin():
            session.add(Post(
                user_id=user_id, 
                post_type=post_type, 
                text=post_text, 
                created_at=datetime.utcnow() + timedelta(hours=3) # Московское время
            ))

    await message.answer(f"Ваш {post_type} пост сохранён!")  
    await state.clear()  


# Обработчик для команды назад и отмена
@router.callback_query(F.data.in_(['back_to_menu', 'cancel']))
async def handle_back_or_cancel(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'back_to_menu':
        await callback.message.edit_text("Вы вернулись в главное меню")
    elif callback.data == 'cancel':
        await state.clear()  # Очистка всех состояний
        await callback.message.edit_text("Вы вернулись в главное меню.")
    
    # В любом случае вызываем show_commands, передавая callback.message
    await show_commands(callback.message)
    
    await callback.answer()