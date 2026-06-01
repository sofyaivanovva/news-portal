"""
Проверка NewsAPIClient против API_BASE_URL.

    API_BASE_URL=https://news-portal--sofyas05604.replit.app python3 -m api_client.verify
"""
import os
import sys
import uuid

import requests

from api_client.client import NewsAPIClient

BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:8000').rstrip('/')
SUFFIX = uuid.uuid4().hex[:8]
USERNAME = f'api_verify_{SUFFIX}'


def check(name, ok, detail=''):
    status = 'OK' if ok else 'FAIL'
    line = f'[{status}] {name}'
    if detail:
        line += f' — {detail}'
    print(line)
    return ok


def probe_api():
    url = f'{BASE_URL}/api/news/'
    try:
        resp = requests.get(url, timeout=15)
    except requests.RequestException as exc:
        return False, f'нет соединения: {exc}'
    if resp.status_code == 404:
        return False, '404 — на сервере нет маршрута /api/ (нужен деплой с REST API)'
    if resp.status_code >= 500:
        return False, f'HTTP {resp.status_code} — ошибка сервера'
    try:
        resp.json()
    except ValueError:
        return False, f'HTTP {resp.status_code} — ответ не JSON'
    return True, f'HTTP {resp.status_code}'


def main():
    print(f'Базовый URL: {BASE_URL}\n')

    api_ok, api_detail = probe_api()
    check('Доступность API (/api/news/)', api_ok, api_detail)
    if not api_ok:
        print('\nПроверка api_client прервана: сервер не отдаёт REST API.')
        sys.exit(1)

    client = NewsAPIClient(BASE_URL)
    all_ok = True

    user = client.register(USERNAME, f'{USERNAME}@example.com', 'securepass123')
    reg_ok = isinstance(user, dict) and user.get('username') == USERNAME
    all_ok &= check('register()', reg_ok, str(user)[:120])

    auth = client.login(USERNAME, 'securepass123')
    login_ok = 'token' in auth
    all_ok &= check('login()', login_ok, 'токен получен' if login_ok else str(auth)[:120])

    content = 'A' * 50 + ' — текст проверки api_client.'
    news = client.create_news(
        title='Проверка API client',
        summary='Краткое описание для verify',
        content=content,
    )
    news_id = news.get('id') if isinstance(news, dict) else None
    create_ok = bool(news_id)
    all_ok &= check('create_news()', create_ok, f'id={news_id}' if create_ok else str(news)[:120])

    if not news_id:
        sys.exit(1)

    listing = client.get_news()
    list_ok = isinstance(listing, dict) and 'results' in listing
    all_ok &= check(
        'get_news() список',
        list_ok,
        f"count={listing.get('count')}" if list_ok else str(listing)[:120],
    )

    one = client.get_news(news_id=news_id)
    one_ok = isinstance(one, dict) and one.get('id') == news_id
    all_ok &= check('get_news(id)', one_ok, one.get('title', '')[:80] if one_ok else str(one)[:120])

    author_id = news.get('author')
    if author_id is not None:
        filtered = client.get_news(author=author_id)
        filt_ok = isinstance(filtered, dict) and filtered.get('count', 0) >= 1
        all_ok &= check(
            'get_news(author=...)',
            filt_ok,
            f"count={filtered.get('count')}" if filt_ok else str(filtered)[:120],
        )

    updated = client.update_news(news_id, title='Заголовок после PATCH')
    upd_ok = isinstance(updated, dict) and updated.get('title') == 'Заголовок после PATCH'
    all_ok &= check('update_news()', upd_ok, updated.get('title', str(updated)[:120]) if isinstance(updated, dict) else str(updated)[:120])

    status = client.delete_news(news_id)
    del_ok = status == 204
    all_ok &= check('delete_news()', del_ok, f'HTTP {status}')

    print()
    if all_ok:
        print('Итог: все проверки пройдены.')
        sys.exit(0)
    print('Итог: есть ошибки.')
    sys.exit(1)


if __name__ == '__main__':
    main()
