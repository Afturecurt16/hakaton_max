# KVS Job для MAX

Бэкенд и мини-приложение KVS Job работают только в MAX. Приложение показывает вакансии и партнёров, поддерживает регистрацию на мероприятия, уведомления, подписку на канал и панель администратора.

## Запуск

1. Создайте `.env` рядом с `config.py`.
2. Укажите `MAX_BOT_TOKEN`, `MAX_ADMIN_IDS` и параметры PostgreSQL.
3. Запустите `docker compose up --build` или `python main.py`.

```env
MAX_BOT_TOKEN=your_max_bot_token
MAX_ADMIN_IDS=123456789
MAX_REQUIRED_CHANNEL_ID=0
MAX_REQUIRED_CHANNEL_URL=
MINIAPP_PUBLIC_URL=https://example.org/miniapp

DB_HOST=localhost
DB_PORT=5432
DB_NAME=kvs_bot
DB_USER=postgres
DB_PASSWORD=postgres
```

Локально мини-приложение открывается по адресу `http://127.0.0.1:8000/miniapp`. Для запуска с PostgreSQL используйте `start-local.ps1`.
