require('dotenv').config();
const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 3000;

// Подключение к БД
const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT,
});

app.use(cors());
app.use(express.json());

// **Добавляем раздачу статических файлов**
app.use(express.static('public'));

app.get("/get-nickname/:tg_id", async (req, res) => {
    const { tg_id } = req.params;
    try {
        const result = await pool.query("SELECT nickname FROM users WHERE tg_id = $1", [tg_id]);
        if (result.rows.length > 0) {
            res.json({ nickname: result.rows[0].nickname });
        } else {
            res.json({ nickname: tg_id }); // Если нет в базе, показываем user_id
        }
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "Database error" });
    }
});

app.get('/posts', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM posts ORDER BY created_at DESC');
        console.log("Все посты из базы данных:", result.rows);  // 👈 Выводим в консоль
        res.json(result.rows);
    } catch (err) {
        console.error("Ошибка при получении всех постов:", err);
        res.status(500).send('Ошибка сервера');
    }
});

app.get('/my-posts/:userId', async (req, res) => {
    const userId = req.params.userId;
    try {
        const result = await pool.query('SELECT * FROM posts WHERE user_id = $1 AND post_type = $2 ORDER BY created_at DESC', [userId, 'private']);
        console.log(`Приватные посты пользователя ${userId}:`, result.rows);  // 👈 Выводим в консоль
        res.json(result.rows);
    } catch (err) {
        console.error(`Ошибка при получении постов пользователя ${userId}:`, err);
        res.status(500).send('Ошибка сервера');
    }
});

app.listen(port, () => {
    console.log(`Сервер запущен на http://localhost:${port}`);
});
