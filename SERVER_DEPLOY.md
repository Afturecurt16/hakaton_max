# Запуск KVS Job на сервере

## 1. Подготовка

На сервере должны быть установлены Docker и Docker Compose.

Распакуйте архив и перейдите в его папку:

```bash
cd kvs_career_bot
cp .env.example .env
nano .env
```

Заполните минимум:

```env
MAX_BOT_TOKEN=токен_бота_MAX
MAX_ADMIN_IDS=ваш_MAX_user_id
MINIAPP_PUBLIC_URL=https://ваш-домен.ru/miniapp
DB_PASSWORD=сложный_пароль
```

Если используются вакансии из Google Sheets, отдельно загрузите в корень проекта файл `credentials.json` и укажите `GOOGLE_SHEETS_URL`.

## 2. Запуск

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f bot
```

Приложение внутри контейнера слушает порт `8000`. Для MAX нужен публичный HTTPS-адрес, например `https://ваш-домен.ru/miniapp`. Настройте reverse proxy (Nginx/Caddy) и сертификат на домене.

## 3. Подключение в MAX

В платформе MAX откройте: **Чат-боты → нужный бот → ⋮ → Настройки**. Укажите URL мини-приложения и включите кнопку запуска.

## 4. Проверка

```bash
curl -I https://ваш-домен.ru/miniapp
docker compose logs --tail=100 bot
```

Не добавляйте в архив `.env`, `credentials.json` и другие секретные файлы.
