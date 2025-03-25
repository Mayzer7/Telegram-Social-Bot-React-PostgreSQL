from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Глобальная reply клавиатура
global_reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Главное меню")]  # Кнопка для возврата на главную
    ],
    resize_keyboard=True  # Автоматически изменять размер клавиатуры
)

my_comands_text = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мои команды", callback_data="my_comands_text")]
])

my_comands = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить пост", callback_data="add_post")],
    [InlineKeyboardButton(text="Показать посты", callback_data="choose_method_view_posts")],
    [InlineKeyboardButton(text="Показать мои посты", callback_data="show_my_posts")],
])

post_categories = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Публичный пост", callback_data="public_post")],
    [InlineKeyboardButton(text="Приватный пост", callback_data="private_post")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")]  # Кнопка возврата
])

cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
])

type_posts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Публичные", callback_data="type_public_posts")],
    [InlineKeyboardButton(text="Приватные", callback_data="type_private_posts")],
])

methods_view_posts = InlineKeyboardMarkup(inline_keyboard=[
    # Кнопка с веб-приложением, сразу открывает ссылку в браузере
    [InlineKeyboardButton(text="В браузере", web_app={"url": "https://72ad-138-124-89-72.ngrok-free.app"})],
    [InlineKeyboardButton(text="В самом тг", callback_data="in_telegram")]
])