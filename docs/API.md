# REST API — News Portal

Базовый URL: `https://<ваш-домен>/api/` (локально: `http://127.0.0.1:8000/api/`)

## Аутентификация

Поддерживаются **Token** и **Session**.

### Получение токена

```http
POST /api/token/
Content-Type: application/json

{
  "username": "user",
  "password": "password"
}
```

Ответ `200`:

```json
{"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee52"}
```

Заголовок для последующих запросов:

```http
Authorization: Token <ваш_токен>
```

## Пользователи `/api/users/`

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| GET | `/api/users/` | Список пользователей | Авторизован |
| POST | `/api/users/` | Регистрация | Все |
| GET | `/api/users/<id>/` | Профиль | Авторизован |
| PUT/PATCH | `/api/users/<id>/` | Обновление | Авторизован |
| DELETE | `/api/users/<id>/` | Удаление | Авторизован |

**POST — регистрация:**

```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepass123"
}
```

## Новости `/api/news/`

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| GET | `/api/news/` | Список (пагинация 10) | Все |
| POST | `/api/news/` | Создание | Авторизован |
| GET | `/api/news/<id>/` | Детали | Все |
| PUT/PATCH | `/api/news/<id>/` | Изменение | Автор |
| DELETE | `/api/news/<id>/` | Удаление | Автор |

**Фильтрация по автору:**

```http
GET /api/news/?author=5
```

**Пример создания:**

```json
{
  "title": "Заголовок новости",
  "summary": "Краткое описание не короче 10 символов",
  "content": "Полный текст новости — минимум 50 символов для прохождения валидации API."
}
```

Поля `author` и `date_created` задаются автоматически.

**Пример ответа:**

```json
{
  "id": 1,
  "title": "Заголовок",
  "summary": "Краткое описание",
  "content": "...",
  "author": 2,
  "author_name": "username",
  "date_created": "2026-06-01T12:00:00Z"
}
```

## Пагинация

Списки возвращаются с пагинацией (10 записей на страницу):

```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/news/?page=2",
  "previous": null,
  "results": [...]
}
```

## Ошибки валидации

HTTP `400`, тело JSON:

```json
{
  "title": ["Это поле обязательно."],
  "content": ["Минимум 50 символов."]
}
```

## Права доступа

- Чтение новостей — без входа.
- Создание новостей — только авторизованные пользователи; автор подставляется из токена/сессии.
- Изменение и удаление — только автор новости.

## Клиентский модуль

```bash
pip install requests
export DEBUG=True  # для локального сервера
python manage.py runserver
python -m api_client.example
```

См. `api_client/client.py` и `api_client/example.py`.
