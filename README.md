# Glossarium REST API

REST API сервис для управления глоссарием технических терминов на базе FastAPI.

## Функциональность

- Получение всех терминов
- Получение термина по ID
- Поиск терминов по ключевому слову
- Добавление нового термина
- Обновление термина
- Удаление термина
- Инициализация базы данных

## Быстрый старт

### Docker

```bash
docker-compose up --build
```

API будет доступен на http://localhost:8000
Swagger UI: http://localhost:8000/docs

## Архитектура

```
glossarium/
├── app/
│   ├── main.py          # FastAPI приложение, основные роуты
│   ├── database.py      # Настройка async SQLAlchemy
│   ├── models.py        # ORM модель TermModel
│   ├── schemas.py       # Pydantic схемы валидации
│   └── routers/
│       └── terms.py     # REST endpoints для терминов
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Технологии

- **Python 3.11**
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy** - ORM (async режим)
- **Pydantic** - валидация данных
- **Uvicorn** - ASGI сервер
- **aiosqlite** - async SQLite драйвер
- **SQLite** - база данных
