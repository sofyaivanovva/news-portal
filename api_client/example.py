"""
Пример использования NewsAPIClient.

Запуск (сервер должен быть запущен на localhost:8000):
    python -m api_client.example
"""
import os

from api_client.client import NewsAPIClient

BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:8000')


def main():
    client = NewsAPIClient(BASE_URL)

    print('=== Регистрация ===')
    user = client.register('api_demo_user', 'demo@example.com', 'securepass123')
    print(user)

    print('\n=== Вход (токен) ===')
    auth = client.login('api_demo_user', 'securepass123')
    print('Токен получен:', 'token' in auth)

    print('\n=== Создание новости ===')
    content = 'A' * 50 + ' — полный текст демонстрационной новости для API.'
    news = client.create_news(
        title='Новость через API',
        summary='Краткое описание демо-новости для REST API',
        content=content,
    )
    print(news)

    news_id = news.get('id')
    if not news_id:
        print('Не удалось создать новость:', news)
        return

    print('\n=== Список новостей ===')
    listing = client.get_news()
    print(f"Всего (с пагинацией): {listing.get('count', len(listing))}")

    print('\n=== Фильтр по автору ===')
    author_id = news.get('author')
    if author_id:
        filtered = client.get_news(author=author_id)
        print(f"Новостей автора {author_id}: {filtered.get('count', '—')}")

    print('\n=== Обновление новости ===')
    updated = client.update_news(news_id, title='Обновлённый заголовок')
    print(updated.get('title', updated))

    print('\n=== Удаление новости ===')
    status = client.delete_news(news_id)
    print(f'HTTP статус удаления: {status}')


if __name__ == '__main__':
    main()
