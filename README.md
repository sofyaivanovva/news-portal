# News Portal

Новостной портал на Django с веб-интерфейсом и REST API (Django REST Framework).

## Возможности

- Регистрация, вход, профиль пользователя
- CRUD новостей в браузере
- REST API: пользователи, новости, токен-аутентификация
- Фильтрация новостей по автору, пагинация, валидация JSON
- Клиент `api_client` для тестирования API через `requests`

## Быстрый старт (локально)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

export DEBUG=True
export SECRET_KEY=dev-secret-key
python manage.py migrate
python manage.py runserver
```

- Сайт: http://127.0.0.1:8000/
- API: http://127.0.0.1:8000/api/
- Админка: http://127.0.0.1:8000/admin/

Создать суперпользователя:

```bash
python manage.py createsuperuser
```

## Тест API клиентом

```bash
# в отдельном терминале, пока runserver запущен
python -m api_client.example
```

Подробнее: [API.md](API.md)

## Переменные окружения

| Переменная | Описание | Пример (продакшен) |
|------------|----------|---------------------|
| `SECRET_KEY` | Секрет Django | случайная строка 50+ символов |
| `DEBUG` | Режим отладки | `False` |
| `ALLOWED_HOSTS` | Разрешённые хосты через запятую | `myapp.onrender.com` |
| `DATABASE_URL` | URL PostgreSQL (Render) | `postgres://...` |

Локально достаточно `DEBUG=True` и при желании `SECRET_KEY`.

## Деплой на Render.com

1. Запушьте репозиторий на GitHub.
2. [Render](https://render.com) → **New Web Service** → подключите репозиторий.
3. Настройки:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn config.wsgi:application --log-file -`
   - Или используйте `bin/start.sh` (миграции + collectstatic + gunicorn).
4. Добавьте PostgreSQL (опционально) и переменную `DATABASE_URL`.
5. Environment:
   - `SECRET_KEY` — сгенерируйте новый ключ
   - `DEBUG=False`
   - `ALLOWED_HOSTS=ваш-сервис.onrender.com`

После деплоя API будет доступно по `https://<ваш-сервис>.onrender.com/api/`.

## Структура проекта

```
news_portal/
├── config/           # settings, urls, wsgi
├── news_app/         # модели, views, serializers, viewsets, api_urls
├── api_client/       # NewsAPIClient + example
├── bin/start.sh      # скрипт запуска для Render
├── requirements.txt
├── Procfile
├── API.md
└── README.md
```

## Git: ветки и релизы

```bash
git checkout -b feature/api
# ... коммиты ...
git tag -a v1.0.0 -m "Release: REST API"
git push origin feature/api --tags
```

На GitHub: **Releases** → **Draft a new release** → выберите тег `v1.0.0`.
