# Telegram bot assist

Этот проект представляет собой систему для управления python-приложениями и отслеживание их работоспособности.

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/Kapysta38/tg-bot-assist.git
    cd tg-bot-assist
    ```

2. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

3. Настройте переменные окружения:
    Создайте файл `.env` в корневой директории проекта и добавьте необходимые переменные окружения. Пример:
    ```env
    SECRET_KEY=your_secret_key
    POSTGRES_SERVER=localhost:port
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=dbname
    ```

4. Выполните миграции базы данных:
    ```sh
    cd api_store
    alembic upgrade head
    cd ..
    ```

## Запуск

### API

1. Перейдите в директорию `api_store` и запустите FastAPI приложение:
    ```sh
    cd api_store
    uvicorn main:app --reload
    ```

### Бот

1. Перейдите в директорию `bot` и запустите бота:
    ```sh
    cd bot
    python run.py
    ```

## Лицензия

Этот проект лицензирован под лицензией MIT. Подробности смотрите в файле `LICENSE`.
