import React, { useState, useEffect, useRef } from 'react';
import { User, Users, UserCircle } from 'lucide-react';
import WebApp from '@twa-dev/sdk';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

type Post = {
  id: number;
  text: string;
  post_type: string;
  user_id: string;
  created_at: string;
  formattedDate: string;
};

interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  photo_url?: string;
}

function App() {
  const [user, setUser] = useState<TelegramUser | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [showUserPosts, setShowUserPosts] = useState(false);
  const [nicknames, setNicknames] = useState<Record<string, string>>({});
  const fetchedUserIds = useRef(new Set<string>());

  useEffect(() => {
    WebApp.ready();
    const initData = WebApp.initData || '';
    if (initData && WebApp.initDataUnsafe.user) {
      setUser(WebApp.initDataUnsafe.user);
    }

    const fetchPosts = async () => {
      try {
        const response = await fetch('http://localhost:3000/posts');
        const data = await response.json();

        const postsWithFormattedDate = data.map((post: any) => ({
          ...post,
          formattedDate: format(new Date(post.created_at), 'd MMMM yyyy HH:mm', { locale: ru }),
        }));

        setPosts(postsWithFormattedDate);
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
      }
    };

    fetchPosts();
  }, []);

  // ✅ Теперь никнеймы загружаются **один раз** при изменении `posts`
  useEffect(() => {
    async function fetchNicknames() {
      const newNicknames: Record<string, string> = {};
      const uniqueUserIds = new Set(posts.map(post => post.user_id));

      const requests = Array.from(uniqueUserIds)
        .filter(userId => !fetchedUserIds.current.has(userId))
        .map(async userId => {
          const response = await fetch(`http://localhost:3000/get-nickname/${userId}`);
          const data = await response.json();
          newNicknames[userId] = data.nickname || userId;
          fetchedUserIds.current.add(userId);
        });

      await Promise.all(requests);
      setNicknames(prev => ({ ...prev, ...newNicknames })); // ✅ Сохраняем старые никнеймы
    }

    if (posts.length > 0) {
      fetchNicknames();
    }
  }, [posts]); // 🔥 Зависимость теперь `posts`, а не `displayedPosts`

  // ✅ Фильтрация `displayedPosts` теперь только в `return`
  const displayedPosts = showUserPosts
    ? posts.filter(post => post.post_type === 'private' && String(post.user_id) === String(user?.id))
    : posts.filter(post => post.post_type === 'public');

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-md text-center">
          <p className="text-gray-600">This app should be opened from Telegram</p>
        </div>
      </div>
    );
  }

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

        {/* Posts Container */}
        <div className="space-y-4">
          {displayedPosts.map(post => (
            <div
              key={post.id}
              className="bg-white/70 backdrop-blur-sm rounded-xl p-4 shadow-lg shadow-indigo-500/10 transition-all duration-300 hover:transform hover:-translate-y-1"
            >
              <div className="flex items-center gap-3 mb-3">
                <UserCircle className="w-10 h-10 text-gray-500" />
                <div>
                  <h3 className="font-medium text-gray-800">
                    {nicknames[post.user_id] || post.user_id}
                  </h3>
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
