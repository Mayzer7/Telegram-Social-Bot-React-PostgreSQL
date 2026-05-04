# Telegram Social Bot 🚀

![Image](https://github.com/user-attachments/assets/20e4bc5e-6b52-4e21-bcf8-e223862bf473)
![Image](https://github.com/user-attachments/assets/b9b7f351-8b14-43a2-9b9a-990882b29a66)

<p align="center">
   ![Image](https://github.com/user-attachments/assets/5def370e-6b82-4229-a069-e171e5a71cc7)
</p>

## Описание

Telegram Social Bot — это асинхронный телеграм-бот, который позволяет пользователям быстро создавать посты, как публичные, так и приватные. Бот поддерживает хранение данных, управление пользователями и удобные кнопки для навигации.

Кроме того, бот включает встроенный веб-сервис на React, который открывается внутри Telegram через встроенный браузер. Этот веб-интерфейс с продуманным UX/UI позволяет пользователям комфортно просматривать как публичные, так и приватные посты друг друга.

## Используемые технологии

- **Python** — основной язык программирования
- **Aiogram** — асинхронный фреймворк для работы с Telegram Bot API
- **React** — веб-сервис
- **PostgreSQL** — база данных для хранения информации
- **Express** - для передачи данных с бд на сайт
- **IMGBB** - внешний облачный сервис для хранения аватарок пользователей
- **asyncio** — асинхронное выполнение задач

## Функционал

- **Регистрация пользователей** 
- **Создание и управление записями** 
- **Поддержка состояний пользователей (FSM)** 
- **Интерактивные клавиатуры**
- **Интеграция с веб-сервисом**

## 🛠 Локальная установка и запуск

### Клонирование репозитория

```bash
git clone https://github.com/Mayzer7/Telegram-Social-Bot-React-PostgreSQL.git
cd Telegram-Social-Bot-React-PostgreSQL
```

### Установка зависимостей

Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv venv
source venv/bin/activate  # для macOS/Linux
venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

### Настройка переменных окружения

Создайте файл `.env` в корневой папке проекта и добавьте:

```
BOT_TOKEN=your_telegram_bot_token

DB_ENGINE=postgresql+asyncpg
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port

IMGBB_API_KEY=your_imgbb_api_key
```

```
Далее нужно создать .env в этой директории: "app/web/server/.env" и добавьте в него:

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
```

### Установка модулей

Перейдите в директорию **app/web/** и выполните команду:

```bash
npm install
```

Затем перейдите в **app/web/server/** и установите зависимости:

```bash
npm install
```

### Запуск

1. **Запуск сервера** (в первой вкладке терминала):

   ```bash
   cd app/web/server
   node server.js
   ```

2. **Сборка и запуск React-приложения** (во второй вкладке терминала):

   ```bash
   cd app/web
   npm run build
   npm run preview
   ```
   
   После этого веб-сайт будет доступен, например, по адресу `localhost:4173`.

3. **Настройка ngrok** (в третьей вкладке терминала):

   ```bash
   ngrok http 4173
   ```
   
   Полученный **ngrok-адрес** нужно указать в коде бота.

4. **Изменение ссылки в клавиатуре бота**

   Откройте файл **app/keyboards.py** и измените параметр `url` в `reply_markup`, заменив `your_ngrok_address` на актуальный адрес:

   ```python
   methods_view_posts = InlineKeyboardMarkup(inline_keyboard=[
       [InlineKeyboardButton(text="В браузере", web_app={"url": "your_ngrok_address"})],
       [InlineKeyboardButton(text="В самом тг", callback_data="in_telegram")]
   ])
   ```

5. **Запуск бота** (в четвертой вкладке терминала):

   ```bash
   cd app
   python bot.py
   ```

Теперь бот полностью готов к использованию! 🚀

## Структура проекта
```
📂 Telegram-Social-Bot-React-PostgreSQL
├── 📂 app
│   ├── 📄 bot.py          # Основной файл бота
│   ├── 📂 database       # Работа с базой данных
│   ├── 📄 handlers.py    # Обработчики команд
│   ├── 📄 keyboards.py   # Клавиатуры для бота
│   ├── 📄 states.py      # FSM состояния
│   ├── 📂 web           # Интеграция с веб-сервисами
├── 📄 .env               # Файл с переменными окружения
├── 📄 .gitignore         # Файл исключения для Git
├── 📄 requirements.txt   # Список зависимостей
└── 📄 README.md          # Документация проекта
```

## Возможные улучшения

- Улучшение логирования и обработки ошибок 
- Добавление аналитики использования бота
- Перенос из хендлеров блоки кода с взаимодействием с базой данных в отдельный файл crud.py для читабельности и ненагромождении кода
