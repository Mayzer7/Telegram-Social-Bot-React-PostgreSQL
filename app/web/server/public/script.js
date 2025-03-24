document.addEventListener("DOMContentLoaded", async function () {
    const allPostsContainer = document.getElementById('all-posts');
    const myPostsContainer = document.getElementById('my-posts');
    const userId = document.getElementById('user-id').textContent.trim();

    try {
        // Загружаем все посты
        const allPostsResponse = await fetch('http://localhost:3000/posts');
        const allPosts = await allPostsResponse.json();

        allPostsContainer.innerHTML = allPosts
            .map(post => `<div class="post"><p>${post.text}</p></div>`)
            .join('');

        // Загружаем только приватные посты пользователя
        const myPostsResponse = await fetch(`http://localhost:3000/my-posts/${userId}`);
        const myPosts = await myPostsResponse.json();

        myPostsContainer.innerHTML = myPosts
            .map(post => `<div class="post private"><p>${post.text}</p></div>`)
            .join('');

    } catch (error) {
        console.error("Ошибка загрузки", error);
        allPostsContainer.innerHTML = "<p>Ошибка загрузки постов</p>";
        myPostsContainer.innerHTML = "<p>Ошибка загрузки постов</p>";
    }
});
