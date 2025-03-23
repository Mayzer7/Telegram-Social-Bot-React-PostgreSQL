from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

my_comands_text = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мои команды", callback_data="my_comands_text")]
])

my_comands = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить пост", callback_data="add_post")],
    [InlineKeyboardButton(text="Показать посты", callback_data="show_all_posts")],
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