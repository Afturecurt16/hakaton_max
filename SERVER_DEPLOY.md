# Публикация KVS Job для MAX

## 1. Подготовка

На сервере должны быть установлены Docker и Docker Compose.

Склонируйте репозиторий или распакуйте финальный архив и перейдите в корень проекта:

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

Если вакансии импортируются из Google Sheets, загрузите в корень проекта файл `credentials.json`, укажите `GOOGLE_SHEETS_URL` и предоставьте сервисному аккаунту доступ к таблице.

## 2. Запуск

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f bot
```

Приложение внутри контейнера слушает порт `8000`. Для MAX нужен публичный HTTPS-адрес, например `https://ваш-домен.ru/miniapp`. Настройте reverse proxy (Nginx/Caddy) и сертификат на домене.

## 3. Подключение в MAX

В платформе MAX настройте у созданного бота кнопку запуска Mini App на публичный HTTPS-адрес из `MINIAPP_PUBLIC_URL`. После этого пользовательский сценарий проходится внутри MAX.

## 4. Проверка

```bash
curl -I https://ваш-домен.ru/miniapp
docker compose logs --tail=100 bot
```

Не добавляйте в Git или финальный архив `.env`, `credentials.json`, токены и Docker-тома. Полные инструкции и сценарий проверки находятся в [README.md](README.md).
