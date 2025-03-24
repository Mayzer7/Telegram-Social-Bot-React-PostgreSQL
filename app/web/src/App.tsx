import React, { useState, useEffect } from 'react';
import { User, Users, UserCircle } from 'lucide-react';
import WebApp from '@twa-dev/sdk';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';


type Post = {
  id: number;
  text: string;
  post_type: string;
  user_id: number;
  created_at: string;
  formattedDate: string; // Добавляем поле для отформатированной даты
};

interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
}

function App() {
  const [user, setUser] = useState<TelegramUser | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [showUserPosts, setShowUserPosts] = useState(false);

  useEffect(() => {
    // Initialize Telegram WebApp
    WebApp.ready();

    // Get user data if available
    const initData = WebApp.initData || '';
    if (initData && WebApp.initDataUnsafe.user) {
      setUser(WebApp.initDataUnsafe.user);
    }

    // Функция для запроса данных с сервера
    const fetchPosts = async () => {
      try {
        const response = await fetch('http://localhost:3000/posts'); // Адрес сервера
        const data = await response.json(); // Преобразуем ответ в JSON

        // Отформатировать дату для каждого поста
        const postsWithFormattedDate = data.map((post: any) => ({
          ...post,
          formattedDate: format(new Date(post.created_at), 'd MMMM yyyy HH:mm', { locale: ru })
        }));
        
        setPosts(postsWithFormattedDate); // Сохраняем данные в состояние
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error); // Логируем ошибку в случае неудачи
      }
    };

    fetchPosts(); // Вызов функции при монтировании компонента
  }, []);

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-md text-center">
          <p className="text-gray-600">This app should be opened from Telegram</p>
        </div>
      </div>
    );
  }

  // Фильтрация постов в зависимости от состояния переключателя
  const displayedPosts = showUserPosts
    ? posts.filter(post => post.post_type === 'private') // Отображаем только приватные посты
    : posts.filter(post => post.post_type === 'public'); // Отображаем только публичные посты

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100 p-4">
      <div className="max-w-md mx-auto space-y-6">
        {/* Toggle Buttons */}
        <div className="flex gap-2 p-2 bg-white/30 backdrop-blur-sm rounded-xl">
          <button
            onClick={() => setShowUserPosts(false)}
            className={`flex-1 py-3 px-4 rounded-lg font-medium text-sm flex items-center justify-center gap-2 transition-all duration-300 ${
              !showUserPosts
                ? 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-lg shadow-indigo-500/30'
                : 'bg-white/50 text-gray-700'
            }`}
          >
            <Users size={18} />
            Все посты
          </button>
          <button
            onClick={() => setShowUserPosts(true)}
            className={`flex-1 py-3 px-4 rounded-lg font-medium text-sm flex items-center justify-center gap-2 transition-all duration-300 ${
              showUserPosts
                ? 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-lg shadow-indigo-500/30'
                : 'bg-white/50 text-gray-700'
            }`}
          >
            <UserCircle size={18} />
            Мои посты
          </button>
        </div>

        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
          <div className="bg-white p-8 rounded-lg shadow-md">
            <div className="flex items-center justify-center mb-6">
              <User className="w-16 h-16 text-blue-500" />
            </div>
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-800 mb-4">Telegram User Info</h1>
              <div className="space-y-2">
                <p className="text-gray-700">
                  <span className="font-semibold">ID:</span> {user.id}
                </p>
                <p className="text-gray-700">
                  <span className="font-semibold">Name:</span>{' '}
                  {user.first_name} {user.last_name}
                </p>
                {user.username && (
                  <p className="text-gray-700">
                    <span className="font-semibold">Username:</span> @{user.username}
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Posts Container */}
        <div className="space-y-4">
          {displayedPosts.map((post) => (
            <div key={post.id}
              className="bg-white/70 backdrop-blur-sm rounded-xl p-4 shadow-lg shadow-indigo-500/10 transition-all duration-300 hover:transform hover:-translate-y-1"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-violet-500 to-indigo-500 flex items-center justify-center text-white font-medium">
                  {/* {post.username} */}
                </div>
                <div>
                  <h3 className="font-medium text-gray-800">{post.user_id}</h3>
                  <p className="text-xs text-gray-500">{post.formattedDate}</p>
                </div>
              </div>
              <p className="text-gray-700 leading-relaxed">{post.text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
