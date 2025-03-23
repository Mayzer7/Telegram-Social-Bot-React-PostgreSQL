from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards import my_comands_text, my_comands, post_categories
from aiogram.fsm.context import FSMContext 
from states import WritePost

router = Router()

@router.message(F.text == '/start')
async def hello(message: Message):
    await message.answer('Привет я бот для заметок', reply_markup=my_comands_text)
    
@router.callback_query(F.data == 'my_comands_text')
async def show_comands(callback: CallbackQuery):
    await callback.message.edit_text("Вот мои команды:", reply_markup=my_comands)

@router.callback_query(F.data == 'add_post')
async def show_add_post(callback: CallbackQuery):
    await callback.message.edit_text("Выберите категорию поста", reply_markup=post_categories)

@router.callback_query(F.data == 'public_post')
async def show_add_post(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Напишите публичный пост")
    await state.set_state(WritePost.waiting_for_text)


@router.message(WritePost.waiting_for_text)
async def receive_post_text(message: Message, state: FSMContext):
    post_text = message.text  # Получаем текст поста
    await message.answer(f"Ваш пост сохранён: {post_text}")  # Отправляем подтверждение
    await state.clear()  # Сбрасываем состояние

# Обработчик для кнопки "Назад"
@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery):
    await show_comands(callback)